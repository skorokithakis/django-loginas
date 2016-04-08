from django.conf import settings

USER_SESSION_FLAG = getattr(settings, "LOGINAS_FROM_USER_SESSION_FLAG", "loginas_from_user")

CAN_LOGIN_AS = getattr(settings, "CAN_LOGIN_AS", lambda r, y: r.user.is_superuser)

LOGIN_REDIRECT = getattr(settings, "LOGINAS_REDIRECT_URL", settings.LOGIN_REDIRECT_URL)
