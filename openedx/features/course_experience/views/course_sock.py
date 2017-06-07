"""
Fragment for rendering the course's verification sock and associated toggle button.
"""
from datetime import datetime

from django.conf import settings
from django.template.loader import render_to_string
from opaque_keys.edx.keys import CourseKey
from web_fragments.fragment import Fragment

from student.models import CourseEnrollment
from course_modes.models import CourseMode
from courseware.date_summary import VerifiedUpgradeDeadlineDate
from courseware.courses import get_course_with_access
from openedx.core.djangoapps.plugin_api.views import EdxFragmentView


class CourseSockFragmentView(EdxFragmentView):
    """
    A fragment to allow users to verify the course from the home page
    """
    def render_to_fragment(self, request, course_id=None, course=None, **kwargs):
        """
        Render the course's verification sock fragment.
        """
        # Establish whether the course has a verified mode
        course_key = CourseKey.from_string(course_id)
        if course is None:
            course = get_course_with_access(request.user, 'load', course_key, check_if_enrolled=True)
        user_course_modes = CourseMode.modes_for_course_dict(course_key)
        available_modes = CourseMode.modes_for_course_dict(course_id)
        has_verified_mode = CourseMode.has_verified_mode(available_modes)

        # Establish whether the user is already enrolled
        is_already_verified = CourseEnrollment.is_enrolled_as_verified(request.user.id, course_key)

        # Establish whether the verification deadline has already passed
        verification_deadline = VerifiedUpgradeDeadlineDate(course, request.user)
        deadline_has_passed = verification_deadline.deadline_has_passed()

        show_course_sock = has_verified_mode and not is_already_verified and not deadline_has_passed

        # Get the price of the course and format correctly
        registration_price = ''
        if show_course_sock:
            # Grab the type of currency and the total cost of the course
            currency = settings.PAID_COURSE_REGISTRATION_CURRENCY[0]
            course_cost = CourseMode.min_course_price_for_currency(course_key, currency)

            # Format the price to zero decimal places if full value, otherwise use two decimal places
            currency_format = "{0}" if course_cost % 1 == 0 else "{0:.2f}"
            amount = currency_format.format(course_cost)
            symbol = '$' if currency == 'usd' else ''
            registration_price = symbol + amount + " " + currency.upper()

        context = {
            'show_course_sock': show_course_sock,
            'course_price': registration_price,
            'course_id': course_id
        }
        html = render_to_string('course_experience/course-sock-fragment.html', context)
        return Fragment(html)
