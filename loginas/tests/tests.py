# -*- coding: utf-8 -*-
from __future__ import unicode_literals, print_function, absolute_import

try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit
from datetime import timedelta

from django.conf import settings as django_settings
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User, update_last_login
from django.contrib.auth.signals import user_logged_in
from django.test.utils import override_settings as override_settings_orig
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.contrib.messages.storage.cookie import CookieStorage
from django.utils.six import text_type
from django.utils import timezone


from loginas import settings as la_settings


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


def create_user(username='', password='', **kwargs):
    user = User(username=username, **kwargs)
    if password:
        user.set_password(password)
    user.save()
    return user


def login_as_nonstaff(request, user):
    return request.user.is_superuser or (request.user.is_staff and
                                         not user.is_staff)


class ViewTest(TestCase):

    """Tests for user_login view"""

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get('/')  # To get the CSRF token for next request
        assert django_settings.CSRF_COOKIE_NAME in self.client.cookies
        self.target_user = User.objects.create(username='target')
        # setup listener
        user_logged_in.connect(update_last_login)

    def tearDown(self):
        """Disconnect the listeners"""
        user_logged_in.disconnect(update_last_login)

    def get_csrf_token_payload(self):
        return {
            'csrfmiddlewaretoken':
                self.client.cookies[django_settings.CSRF_COOKIE_NAME].value
        }

    def get_target_url(self, target_user=None):
        if target_user is None:
            target_user = self.target_user
        response = self.client.post(
            reverse("loginas-user-login", kwargs={'user_id': target_user.id}),
            data=self.get_csrf_token_payload()
        )
        self.assertEqual(response.status_code, 302)
        return response

    def assertCurrentUserIs(self, user):
        id_ = text_type(user.id if user is not None else None).encode('utf-8')
        r = self.client.post(
            reverse("current_user"),
            data=self.get_csrf_token_payload()
        )
        self.assertEqual(r.content, id_)

    def assertLoginError(self, resp):
        self.assertEqual(urlsplit(resp['Location'])[2], "/")

        messages = CookieStorage(resp)._decode(resp.cookies['messages'].value)
        self.assertIn(
            (40, "You do not have permission to do that."),
            [(m.level, m.message) for m in messages]
        )

    def assertLoginSuccess(self, resp, user):
        self.assertEqual(urlsplit(resp['Location'])[2],
                         django_settings.LOGIN_REDIRECT_URL)
        msg = la_settings.MESSAGE_LOGIN_SWITCH.format(username=user.username)
        messages = CookieStorage(resp)._decode(resp.cookies['messages'].value)
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
        user = create_user(u"üser", "pass", is_superuser=False, is_staff=False)
        staff1 = create_user("stäff", "pass", is_superuser=False, is_staff=True)
        staff2 = create_user("super", "pass", is_superuser=True, is_staff=True)

        # Regular user can't login as anyone
        self.assertTrue(self.client.login(username=u"üser", password="pass"))
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

    @override_settings(CAN_LOGIN_AS='loginas.tests.login_as_shorter_username')
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
            self.assertRaisesExact(
                ImproperlyConfigured(message),
                self.get_target_url
            )
        with override_settings(CAN_LOGIN_AS='loginas.tests.invalid_func'):
            assertMessage(
                "Module loginas.tests does not define a invalid_func function.")
        with override_settings(CAN_LOGIN_AS='loginas.tests.invalid_path.func'):
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

    def test_as_anonymous_user(self):
        self.assertLoginError(self.get_target_url())
        self.assertCurrentUserIs(None)

    def test_get_405_method_not_allowed(self):
        url = reverse("loginas-user-login", kwargs={'user_id': '0'})
        r = self.client.get(url)
        self.assertEqual(r.status_code, 405)

    def test_missing_csrf_token_403_forbidden(self):
        url = reverse("loginas-user-login", kwargs={'user_id': '0'})
        r = self.client.post(url)
        self.assertEqual(r.status_code, 403)

    @override_settings(LOGINAS_REDIRECT_URL="/another-redirect")
    def test_loginas_redirect_url(self):
        create_user("me", "pass", is_superuser=True, is_staff=True)
        self.assertTrue(self.client.login(username="me", password="pass"))

        response = self.client.post(
            reverse("loginas-user-login", kwargs={'user_id': self.target_user.id}),
            data=self.get_csrf_token_payload()
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlsplit(response['Location'])[2], "/another-redirect")

    def test_restore_original_user(self):

        # Create a super user and login as this
        original_user = create_user("me", "pass", is_superuser=True, is_staff=True)
        self.assertTrue(self.client.login(username="me", password="pass"))
        response = self.get_target_url()
        self.assertLoginSuccess(response, self.target_user)

        url = reverse("loginas-user-login", kwargs={'user_id': self.target_user.id})
        self.client.get(url)
        self.assertCurrentUserIs(self.target_user)

        # Restore
        url = reverse("loginas-logout")
        self.client.get(url)
        self.assertCurrentUserIs(original_user)

    @override_settings(LOGINAS_LOGOUT_REDIRECT_URL="/another-redirect")
    def test_loginas_redirect_url(self):
        create_user("me", "pass", is_superuser=True, is_staff=True)
        self.assertTrue(self.client.login(username="me", password="pass"))
        response = self.client.get(reverse("loginas-logout"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlsplit(response['Location'])[2], "/another-redirect")

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
