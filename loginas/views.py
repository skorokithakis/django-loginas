try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module

from django.contrib import messages
from django.core.exceptions import ImproperlyConfigured
from django.shortcuts import redirect
from django.utils import six
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.http import require_POST
from django.utils.translation import ugettext_lazy as _

from .utils import login_as, restore_original_login
from . import settings as la_settings


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
        raise ImproperlyConfigured(
            'Error importing CAN_LOGIN_AS function: {}'.format(module)
        )
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


@csrf_protect
@require_POST
def user_login(request, user_id):
    user = User.objects.get(pk=user_id)

    if isinstance(la_settings.CAN_LOGIN_AS, six.string_types):
        can_login_as = _load_module(la_settings.CAN_LOGIN_AS)
    elif hasattr(la_settings.CAN_LOGIN_AS, "__call__"):
        can_login_as = la_settings.CAN_LOGIN_AS
    else:
        raise ImproperlyConfigured("The CAN_LOGIN_AS setting is neither a valid module nor callable.")

    if user.is_superuser:
        messages.error(request, _("You cannot log in as superusers."),
                       extra_tags=la_settings.MESSAGE_EXTRA_TAGS)
        return redirect(request.META.get("HTTP_REFERER", "/"))

    if not can_login_as(request, user):
        messages.error(request, _("You do not have permission to do that."),
                       extra_tags=la_settings.MESSAGE_EXTRA_TAGS)
        return redirect(request.META.get("HTTP_REFERER", "/"))

    login_as(user, request)

    return redirect(la_settings.LOGIN_REDIRECT)


def user_logout(request):
    """
    This can replace your default logout view. In you settings, do:

    from django.core.urlresolvers import reverse_lazy
    LOGOUT_URL = reverse_lazy('loginas-logout')
    """
    restore_original_login(request)

    return redirect(la_settings.LOGOUT_REDIRECT)
