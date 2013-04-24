from django.conf import settings
from django.contrib import messages
from django.contrib.auth import load_backend, login
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.utils.importlib import import_module
try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User


def _load_module(path):
    """Code to load create user module. Copied off django-browserid."""

    i = path.rfind('.')
    module, attr = path[:i], path[i + 1:]

    try:
        mod = import_module(module)
    except ImportError:
        raise ImproperlyConfigured('Error importing CAN_LOGIN_AS'
                                   ' function.')
    except ValueError:
        raise ImproperlyConfigured('Error importing CAN_LOGIN_AS'
                                   ' function. Is CAN_LOGIN_AS a'
                                   ' string?')

    try:
        can_login_as = getattr(mod, attr)
    except AttributeError:
        raise ImproperlyConfigured('Module {0} does not define a {1} '
                                   'function.'.format(module, attr))
    return can_login_as


def user_login(request, user_id):
    user = User.objects.get(pk=user_id)

    CAN_LOGIN_AS = getattr(settings, "CAN_LOGIN_AS", lambda r, y: r.user.is_superuser)
    if isinstance(CAN_LOGIN_AS, basestring):
        can_login_as = _load_module(CAN_LOGIN_AS)
    elif hasattr(CAN_LOGIN_AS, "__call__"):
        can_login_as = CAN_LOGIN_AS
    else:
        raise ImproperlyConfigured("The CAN_LOGIN_AS setting is neither a valid module nor callable.")

    if not can_login_as(request, user):
        messages.error(request, "You do not have permission to do that.")
        return redirect(request.META.get("HTTP_REFERER", "/"))

    # Find a suitable backend.
    if not hasattr(user, 'backend'):
        for backend in settings.AUTHENTICATION_BACKENDS:
            if user == load_backend(backend).get_user(user.pk):
                user.backend = backend
                break

    # Log the user in.
    if hasattr(user, 'backend'):
        login(request, user)

    return redirect("/")
