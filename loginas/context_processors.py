from loginas.utils import is_impersonated_session


def impersonated_session_status(request):
    """
    Adds variable to all contexts
    :param request:
    :return bool:
    """
    return {"is_impersonated_session": is_impersonated_session(request)}
