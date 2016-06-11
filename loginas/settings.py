from django.conf import settings

USER_SESSION_FLAG = getattr(settings, "LOGINAS_FROM_USER_SESSION_FLAG", "loginas_from_user")

CAN_LOGIN_AS = getattr(settings, "CAN_LOGIN_AS", lambda r, y: r.user.is_superuser)

LOGIN_REDIRECT = getattr(settings, "LOGINAS_REDIRECT_URL", settings.LOGIN_REDIRECT_URL)

MESSAGE_LOGIN_SWITCH = getattr(
    settings,
    "LOGINAS_MESSAGE_LOGIN_SWITCH",
    u"Your login is now switched to {username} - log out to become your original user!"
)

MESSAGE_LOGIN_REVERT = getattr(
    settings,
    "MESSAGE_LOGIN_REVERT",
    u"You are now logged back in as {username}"
)
