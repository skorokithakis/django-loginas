import logging
from datetime import timedelta

from django.conf import settings as django_settings
from django.contrib import messages
from django.contrib.admin.models import CHANGE, LogEntry
from django.contrib.auth import get_user_model, load_backend, login, logout
from django.contrib.auth.models import update_last_login
from django.contrib.auth.signals import user_logged_in
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ImproperlyConfigured
from django.core.signing import SignatureExpired, TimestampSigner

from . import settings as la_settings

signer = TimestampSigner()
logger = logging.getLogger(__name__)
username_field = la_settings.USERNAME_FIELD


def login_as(user, request, store_original_user=True):
    """
    Utility function for forcing a login as specific user -- be careful about
    calling this carelessly :)
    """

    # Save the original user pk before it is replaced in the login method
    original_user_pk = request.user.pk

    # Find a suitable backend.
    if not hasattr(user, "backend"):
        for backend in django_settings.AUTHENTICATION_BACKENDS:
            if not hasattr(load_backend(backend), "get_user"):
                continue

            if user == load_backend(backend).get_user(user.pk):
                user.backend = backend
                break
        else:
            raise ImproperlyConfigured("Could not found an appropriate authentication backend")

    # Add admin audit log entry
    change_message = "User {0} logged in as {1}.".format(request.user, user)
    LogEntry.objects.log_action(
        user_id=original_user_pk,
        content_type_id=ContentType.objects.get_for_model(user).pk,
        object_id=user.pk,
        object_repr=str(user),
        change_message=change_message,
        action_flag=CHANGE,
    )

    # Log the user in.
    if hasattr(user, "backend"):
        signal_was_connected = False
        if not la_settings.UPDATE_LAST_LOGIN:
            # Prevent update of user last_login
            signal_was_connected = user_logged_in.disconnect(update_last_login)

        try:
            # Actually log user in
            login(request, user)
        finally:
            # Restore signal if needed
            if signal_was_connected:
                user_logged_in.connect(update_last_login)
    else:
        return

    # Set a flag on the session
    if store_original_user:
        messages.warning(
            request,
            la_settings.MESSAGE_LOGIN_SWITCH.format(username=user.__dict__[username_field]),
            extra_tags=la_settings.MESSAGE_EXTRA_TAGS,
        )
        request.session[la_settings.USER_SESSION_FLAG] = signer.sign(original_user_pk)


def restore_original_login(request):
    """
    Restore an original login session, checking the signed session
    """
    original_session = request.session.get(la_settings.USER_SESSION_FLAG)
    logout(request)

    if not original_session:
        return

    try:
        original_user_pk = signer.unsign(
            original_session, max_age=timedelta(days=la_settings.USER_SESSION_DAYS_TIMESTAMP).total_seconds()
        )
        user = get_user_model().objects.get(pk=original_user_pk)
        messages.info(
            request,
            la_settings.MESSAGE_LOGIN_REVERT.format(username=user.__dict__[username_field]),
            extra_tags=la_settings.MESSAGE_EXTRA_TAGS,
        )
        login_as(user, request, store_original_user=False)
        if la_settings.USER_SESSION_FLAG in request.session:
            del request.session[la_settings.USER_SESSION_FLAG]
    except SignatureExpired:
        pass


def is_impersonated_session(request):
    """
    Checks if the session in the request is impersonated or not
    """
    return la_settings.USER_SESSION_FLAG in request.session
