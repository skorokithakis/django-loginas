from django.conf import settings # import the settings file
from loginas.utils import is_impersonated_session


def impersonated_session_status(request):
    """
    Adds variable to all contexts
    :param request:
    :return bool:
    """
    try:
        is_impersonated = is_impersonated_session(request)
    except:
        is_impersonated = False
    return { 'is_impersonated_session': is_impersonated }