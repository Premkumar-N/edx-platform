"""
Module to define url helpers functions
"""
from urllib import urlencode

from django.core.urlresolvers import reverse

from xmodule.modulestore.django import modulestore
from xmodule.modulestore.search import navigation_index, path_to_location


# TODO: TNL-6547: Remove unified_course_view parameter
def get_redirect_url(course_key, usage_key, unified_course_view=False):
    """ Returns the redirect url back to courseware

    Args:
        course_id(str): Course Id string
        location(str): The location id of course component
        unified_course_view (bool): temporary parameter while this feature is behind a waffle flag.
            Is the unified_course_view waffle flag on?

    Raises:
        ItemNotFoundError if no data at the location or NoPathToItem if location not in any class

    Returns:
        Redirect url string
    """
    if usage_key.block_type == 'course' and unified_course_view:
        return reverse('openedx.course_experience.course_home', args=[unicode(course_key)])

    (
        course_key, chapter, section, vertical_unused,
        position, final_target_id
    ) = path_to_location(modulestore(), usage_key)

    # choose the appropriate view (and provide the necessary args) based on the
    # args provided by the redirect.
    # Rely on index to do all error handling and access control.
    if chapter is None:
        redirect_url = reverse('courseware', args=(unicode(course_key), ))
    elif section is None:
        redirect_url = reverse('courseware_chapter', args=(unicode(course_key), chapter))
    elif position is None:
        redirect_url = reverse(
            'courseware_section',
            args=(unicode(course_key), chapter, section)
        )
    else:
        # Here we use the navigation_index from the position returned from
        # path_to_location - we can only navigate to the topmost vertical at the
        # moment
        redirect_url = reverse(
            'courseware_position',
            args=(unicode(course_key), chapter, section, navigation_index(position))
        )
    redirect_url += "?{}".format(urlencode({'activate_block_id': unicode(final_target_id)}))
    return redirect_url
