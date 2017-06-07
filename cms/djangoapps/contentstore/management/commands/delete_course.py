"""
    Command for deleting courses

    Arguments:
        arg1 (str): Course key of the course to delete

    Returns:
        none
"""
from django.core.management.base import BaseCommand, CommandError
from opaque_keys import InvalidKeyError
from opaque_keys.edx.keys import CourseKey

from contentstore.utils import delete_course
from xmodule.modulestore import ModuleStoreEnum
from xmodule.modulestore.django import modulestore

from .prompt import query_yes_no


class Command(BaseCommand):
    """
    Delete a MongoDB backed course
    Example usage:
        $ ./manage.py cms delete_course 'course-v1:edX+DemoX+Demo_Course' --settings=devstack
        $ ./manage.py cms delete_course 'course-v1:edX+DemoX+Demo_Course' --keep-instructors --settings=devstack

    """
    help = '''Delete a MongoDB backed course'''

    def add_arguments(self, parser):
        """
        Add arguments to the command parser.
        """
        parser.add_argument('course_key', help="ID of the course to delete.")

        parser.add_argument(
            '--keep-instructors',
            action='store_true',
            default=False,
            help='Specify whether to remove instructors from course or not, default is True.',
        )

    def handle(self, *args, **options):
        try:
            course_key = CourseKey.from_string(options['course_key'])
        except InvalidKeyError:
            raise CommandError("Invalid course_key: '%s'." % options['course_key'])

        if not modulestore().get_course(course_key):
            raise CommandError("Course with '%s' key not found." % options['course_key'])

        print 'Going to delete the %s course from DB....' % options['course_key']
        if query_yes_no("Deleting course {0}. Confirm?".format(course_key), default="no"):
            if query_yes_no("Are you sure. This action cannot be undone!", default="no"):
                delete_course(course_key, ModuleStoreEnum.UserID.mgmt_command, options['keep_instructors'])
                print "Deleted course {}".format(course_key)
