from django.conf import settings
from django.utils.translation import ugettext_lazy as _

USER_SESSION_FLAG = getattr(settings, "LOGINAS_FROM_USER_SESSION_FLAG", "loginas_from_user")

USER_SESSION_DAYS_TIMESTAMP = getattr(settings, "LOGINAS_USER_SESSION_DAYS_TIMESTAMP", 2)

CAN_LOGIN_AS = getattr(settings, "CAN_LOGIN_AS", lambda r, y: r.user.is_superuser)

LOGIN_REDIRECT = getattr(settings, "LOGINAS_REDIRECT_URL", settings.LOGIN_REDIRECT_URL)

LOGOUT_REDIRECT = getattr(settings, "LOGINAS_LOGOUT_REDIRECT_URL", settings.LOGIN_REDIRECT_URL)

MESSAGE_LOGIN_SWITCH = getattr(
    settings,
    "LOGINAS_MESSAGE_LOGIN_SWITCH",
    _("Your login is now switched to {username} - log out to become your original user!")
)

MESSAGE_LOGIN_REVERT = getattr(
    settings,
    "LOGINAS_MESSAGE_LOGIN_REVERT",
    _("You are now logged back in as {username}.")
)

UPDATE_LAST_LOGIN = getattr(settings, 'LOGINAS_UPDATE_LAST_LOGIN', False)

MESSAGE_EXTRA_TAGS = getattr(settings, 'LOGINAS_MESSAGE_EXTRA_TAGS', '')