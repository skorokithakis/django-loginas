try:
    from urllib.parse import urlsplit
except ImportError:
    from urlparse import urlsplit

from django.conf import settings
from django.test import Client
from django.test import TestCase
from django.contrib.auth.models import User
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.contrib.messages.storage.cookie import CookieStorage
from django.utils.six import text_type


def create_user(username='', password='', **kwargs):
    user = User(username=username, **kwargs)
    if password:
        user.set_password(password)
    user.save()
    return user


class ViewTest(TestCase):

    """Tests for user_login view"""

    def login_as_nonstaff(request, user):
        return request.user.is_superuser or (request.user.is_staff and
                                             not user.is_staff)

    def setUp(self):
        self.client = Client(enforce_csrf_checks=True)
        self.client.get('/')  # To get the CSRF token for next request
        assert settings.CSRF_COOKIE_NAME in self.client.cookies
        self.target_user = User.objects.create(username='target')

    def get_csrf_token_payload(self):
        return {
            'csrfmiddlewaretoken':
                self.client.cookies[settings.CSRF_COOKIE_NAME].value
        }

    def get_target_url(self, target_user=None):
        if target_user is None:
            target_user = self.target_user
        response = self.client.post(reverse("loginas-user-login",
            kwargs={'user_id': target_user.id}),
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
            (40, u"You do not have permission to do that."),
            [(m.level, m.message) for m in messages]
        )

    def assertLoginSuccess(self, resp):
        self.assertEqual(urlsplit(resp['Location'])[2],
                         settings.LOGIN_REDIRECT_URL)
        self.assertNotIn('messages', resp.cookies)

    def assertRaisesExact(self, exception, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            self.assertFail("{0} not raised".format(exception))
        except exception.__class__ as caught:
            self.assertEqual(caught.args, exception.args)

    def clear_session_cookie(self):
        del self.client.cookies[settings.SESSION_COOKIE_NAME]

    @override_settings(CAN_LOGIN_AS=login_as_nonstaff)
    def test_custom_permissions(self):
        user = create_user("user", "pass", is_superuser=False, is_staff=False)
        staff1 = create_user("staff", "pass", is_superuser=False, is_staff=True)
        staff2 = create_user("super", "pass", is_superuser=True, is_staff=True)

        # Regular user can't login as anyone
        self.assertTrue(self.client.login(username="user", password="pass"))
        self.assertLoginError(self.get_target_url())
        self.assertCurrentUserIs(user)
        self.clear_session_cookie()

        # Non-superuser staff user can login as regular user
        self.assertTrue(self.client.login(username="staff", password="pass"))
        response = self.get_target_url(user)
        self.assertLoginSuccess(response)
        self.assertCurrentUserIs(user)
        self.clear_session_cookie()

        # Non-superuser staff user cannot login as other staff
        self.assertTrue(self.client.login(username="staff", password="pass"))
        self.assertLoginError(self.get_target_url(staff2))
        self.assertCurrentUserIs(staff1)
        self.clear_session_cookie()

        # Superuser staff user can login as other staff
        self.assertTrue(self.client.login(username="super", password="pass"))
        response = self.get_target_url(staff1)
        self.assertLoginSuccess(response)
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
        self.assertLoginSuccess(response)
        self.assertCurrentUserIs(ray)

    def test_custom_permissions_invalid_path(self):
        def assertMessage(message):
            self.assertRaisesExact(ImproperlyConfigured(message),
                self.get_target_url)
        with override_settings(CAN_LOGIN_AS='loginas.tests.invalid_func'):
            assertMessage("Module loginas.tests does not define a invalid_func "
                    "function.")
        with override_settings(CAN_LOGIN_AS='loginas.tests.invalid_path.func'):
            assertMessage("Error importing CAN_LOGIN_AS function.")

    def test_as_superuser(self):
        create_user("me", "pass", is_superuser=True, is_staff=True)
        self.assertTrue(self.client.login(username="me", password="pass"))
        response = self.get_target_url()
        self.assertLoginSuccess(response)
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

    @override_settings(LOGINAS_REDIRECT_URL="/loginas-redirect")
    def test_loginas_redirect_url(self):
        create_user("me", "pass", is_superuser=True, is_staff=True)
        self.assertTrue(self.client.login(username="me", password="pass"))

        response = self.client.post(reverse("loginas-user-login",
            kwargs={'user_id': self.target_user.id}),
            data=self.get_csrf_token_payload()
        )
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlsplit(response['Location'])[2], "/loginas-redirect")
