# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

import unittest
from datetime import timedelta

import django
from django.conf import settings as django_settings
from django.contrib.auth.models import User
from django.contrib.messages.storage.cookie import CookieStorage
from django.core.exceptions import ImproperlyConfigured, PermissionDenied
from django.test import Client, TestCase
from django.test.utils import override_settings as override_settings_orig
from django.utils import timezone
from django.utils.six import text_type
from loginas import settings as la_settings

try:
    from django.core.urlresolvers import reverse
except ImportError:
    from django.urls import reverse

try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit  # type: ignore


try:
    import imp

    reload = imp.reload  # @ReservedAssignment
except ImportError:
    pass


class override_settings(override_settings_orig):
    """
    Reload application settings module every time we redefine a setting
    """

    def enable(self):
        super(override_settings, self).enable()
        from loginas import settings as loginas_settings

        reload(loginas_settings)

    def disable(self):
        super(override_settings, self).disable()
        from loginas import settings as loginas_settings

        reload(loginas_settings)


def create_user(username="", password="", **kwargs):
    user = User(username=username, **kwargs)
    if password:
        user.set_password(password)
    user.save()
    return user


def login_as_nonstaff(request, user):
    return request.user.is_superuser or (request.user.is_staff and not user.is_staff)


def can_login_as_always_raise_permission_denied(request, user):
    raise PermissionDenied("You can't login as target user")


class WrongAuthBackend:
    """
    An authentication backend is a class that implements two required methods: get_user(user_id) and
    authenticate(**credentials). Unfortunately, some libraries don't comply with this interface (e.g.
    `django-rules` with ObjectPermissionBackend) and omit the required `get_user` method.
    """
    def authenticate(self, *args, **kwargs):
        return None


class ViewTest(TestCase):

    """Tests for user_login view"""

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get("/")  # To get the CSRF token for next request
        assert django_settings.CSRF_COOKIE_NAME in self.client.cookies
        self.target_user = User.objects.create(username="target")

    def get_csrf_token_payload(self):
        return {"csrfmiddlewaretoken": self.client.cookies[django_settings.CSRF_COOKIE_NAME].value}

    def get_target_url(self, target_user=None):
        if target_user is None:
            target_user = self.target_user
        response = self.client.post(
            reverse("loginas-user-login", kwargs={"user_id": target_user.id}), data=self.get_csrf_token_payload()
        )
        self.assertEqual(response.status_code, 302)
        return response

    def assertCurrentUserIs(self, user):
        id_ = text_type(user.id if user is not None else None).encode("utf-8")
        r = self.client.post(reverse("current_user"), data=self.get_csrf_token_payload())
        self.assertEqual(r.content, id_)

    def assertLoginError(self, resp, message=None):
        self.assertEqual(urlsplit(resp["Location"])[2], "/")
        message = message or "You do not have permission to do that."
        messages = CookieStorage(resp)._decode(resp.cookies["messages"].value)
        self.assertIn((40, message), [(m.level, m.message) for m in messages])

    def assertLoginSuccess(self, resp, user):
        self.assertEqual(urlsplit(resp["Location"])[2], django_settings.LOGIN_REDIRECT_URL)
        msg = la_settings.MESSAGE_LOGIN_SWITCH.format(username=user.__dict__[la_settings.USERNAME_FIELD])
        messages = CookieStorage(resp)._decode(resp.cookies["messages"].value)
        self.assertIn(msg, "".join([m.message for m in messages]))

    def assertRaisesExact(self, exception, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            self.assertFail("{0} not raised".format(exception))
        except exception.__class__ as caught:
            self.assertEqual(caught.args, exception.args)

    def clear_session_cookie(self):
        del self.client.cookies[django_settings.SESSION_COOKIE_NAME]

    @override_settings(CAN_LOGIN_AS=login_as_nonstaff)
    def test_custom_permissions(self):
        user = create_user("üser", "pass", is_superuser=False, is_staff=False)
        staff1 = create_user("stäff", "pass", is_superuser=False, is_staff=True)
        staff2 = create_user("super", "pass", is_superuser=True, is_staff=True)

        # Regular user can't login as anyone
        self.assertTrue(self.client.login(username="üser", password="pass"))
        self.assertLoginError(self.get_target_url())
        self.assertCurrentUserIs(user)
        self.clear_session_cookie()

        # Non-superuser staff user can login as regular user
        self.assertTrue(self.client.login(username="stäff", password="pass"))
        response = self.get_target_url(user)
        self.assertLoginSuccess(response, user)
        self.assertCurrentUserIs(user)
        self.clear_session_cookie()

        # Non-superuser staff user cannot login as other staff
        self.assertTrue(self.client.login(username="stäff", password="pass"))
        self.assertLoginError(self.get_target_url(staff2))
        self.assertCurrentUserIs(staff1)
        self.clear_session_cookie()

        # Superuser staff user can login as other staff
        self.assertTrue(self.client.login(username="super", password="pass"))
        response = self.get_target_url(staff1)
        self.assertLoginSuccess(response, staff1)
        self.assertCurrentUserIs(staff1)

    @override_settings(CAN_LOGIN_AS="loginas.tests.login_as_shorter_username")
    def test_custom_permissions_as_string(self):
        ray = create_user("ray", "pass")
        lonnie = create_user("lonnie", "pass")

        # Ray cannot login as Lonnie
        self.assertTrue(self.client.login(username="ray", password="pass"))
        self.assertLoginError(self.get_target_url(lonnie))
        self.assertCurrentUserIs(ray)
        self.clear_session_cookie()

        # Lonnie can login as Ray
        self.assertTrue(self.client.login(username="lonnie", password="pass"))
        response = self.get_target_url(ray)
        self.assertLoginSuccess(response, ray)
        self.assertCurrentUserIs(ray)

    def test_custom_permissions_invalid_path(self):
        def assertMessage(message):
            self.assertRaisesExact(ImproperlyConfigured(message), self.get_target_url)

        with override_settings(CAN_LOGIN_AS="loginas.tests.invalid_func"):
            assertMessage("Module loginas.tests does not define a invalid_func function.")
        with override_settings(CAN_LOGIN_AS="loginas.tests.invalid_path.func"):
            assertMessage("Error importing CAN_LOGIN_AS function: loginas.tests.invalid_path")

    def test_as_superuser(self):
        create_user("me", "pass", is_superuser=True, is_staff=True)
        self.assertTrue(self.client.login(username="me", password="pass"))
        response = self.get_target_url()
        self.assertLoginSuccess(response, self.target_user)
        self.assertCurrentUserIs(self.target_user)

    def test_as_non_superuser(self):
        user = create_user("me", "pass", is_staff=True)
        self.assertTrue(self.client.login(username="me", password="pass"))
        self.assertLoginError(self.get_target_url())
        self.assertCurrentUserIs(user)

    @unittest.skipIf(django.VERSION[:2] < (1, 10), "Django < 1.10 allows to authenticate as inactive user")
    def test_auth_backends_user_not_found(self):
        superuser = create_user("me", "pass", is_superuser=True, is_staff=True)
        self.assertTrue(self.client.login(username="me", password="pass"))
        self.assertCurrentUserIs(superuser)
        # ModelBackend should authenticate superuser but prevent this action for inactive user
        inactive_user = create_user("name", "pass", is_active=False)
        with self.settings(AUTHENTICATION_BACKENDS=('django.contrib.auth.backends.ModelBackend',
                                                    'tests.WrongAuthBackend',)):
            message = "Could not find an appropriate authentication backend"
            self.assertLoginError(self.get_target_url(target_user=inactive_user), message=message)
        self.assertCurrentUserIs(superuser)

    @override_settings(CAN_LOGIN_AS=can_login_as_always_raise_permission_denied)
    def test_can_login_as_permission_denied(self):
        message = "You can't login as target user"
        self.assertLoginError(self.get_target_url(), message=message)

    def test_as_anonymous_user(self):
        self.assertLoginError(self.get_target_url())
        self.assertCurrentUserIs(None)

    def test_get_405_method_not_allowed(self):
        url = reverse("loginas-user-login", kwargs={"user_id": "0"})
        r = self.client.get(url)
        self.assertEqual(r.status_code, 405)

    def test_missing_csrf_token_403_forbidden(self):
        url = reverse("loginas-user-login", kwargs={"user_id": "0"})
        r = self.client.post(url)
        self.assertEqual(r.status_code, 403)

    @override_settings(LOGINAS_REDIRECT_URL="/another-redirect")
    def test_loginas_redirect_url(self):
        create_user("me", "pass", is_superuser=True, is_staff=True)
        self.assertTrue(self.client.login(username="me", password="pass"))

        response = self.client.post(
            reverse("loginas-user-login", kwargs={"user_id": self.target_user.id}), data=self.get_csrf_token_payload()
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlsplit(response["Location"])[2], "/another-redirect")

    def test_restore_original_user(self):

        # Create a super user and login as this
        original_user = create_user("me", "pass", is_superuser=True, is_staff=True)
        self.assertTrue(self.client.login(username="me", password="pass"))
        response = self.get_target_url()
        self.assertLoginSuccess(response, self.target_user)

        url = reverse("loginas-user-login", kwargs={"user_id": self.target_user.id})
        self.client.get(url)
        self.assertCurrentUserIs(self.target_user)

        # Restore
        url = reverse("loginas-logout")
        self.client.get(url)
        self.assertCurrentUserIs(original_user)

    @override_settings(LOGINAS_LOGOUT_REDIRECT_URL="/another-redirect")
    def test_loginas_redirect_url_again(self):
        create_user("me", "pass", is_superuser=True, is_staff=True)
        self.assertTrue(self.client.login(username="me", password="pass"))
        response = self.client.get(reverse("loginas-logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlsplit(response["Location"])[2], "/another-redirect")

    def test_last_login_not_updated(self):
        last_login = timezone.now() - timedelta(hours=1)
        self.target_user.last_login = last_login
        self.target_user.save()
        create_user("me", "pass", is_superuser=True, is_staff=True)
        self.assertTrue(self.client.login(username="me", password="pass"))
        response = self.get_target_url()
        self.assertLoginSuccess(response, self.target_user)
        self.assertCurrentUserIs(self.target_user)
        target_user = User.objects.get(id=self.target_user.id)  # refresh from db
        self.assertEqual(target_user.last_login, last_login)

    @override_settings(LOGINAS_UPDATE_LAST_LOGIN=True)
    def test_last_login_updated(self):
        last_login = timezone.now() - timedelta(hours=1)
        self.target_user.last_login = last_login
        self.target_user.save()
        create_user("me", "pass", is_superuser=True, is_staff=True)
        self.assertTrue(self.client.login(username="me", password="pass"))
        response = self.get_target_url()
        self.assertLoginSuccess(response, self.target_user)
        self.assertCurrentUserIs(self.target_user)
        target_user = User.objects.get(id=self.target_user.id)  # refresh from db
        self.assertGreater(target_user.last_login, last_login)

    @override_settings(USERNAME_FIELD="email")
    def test_custom_username_field(self):
        create_user("me", "pass", is_superuser=True, is_staff=True)
        self.assertTrue(self.client.login(username="me", password="pass"))
        self.target_user.email = "target@loginas.org"
        self.target_user.save()
        response = self.get_target_url()
        self.assertLoginSuccess(response, self.target_user)
