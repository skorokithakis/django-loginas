from urlparse import urlsplit

from django.test import TestCase
from django.contrib.auth.models import User
from django.test.utils import override_settings
from django.core.urlresolvers import reverse
from django.core.exceptions import ImproperlyConfigured
from django.contrib.messages.storage.cookie import CookieStorage


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
        self.target_user = User.objects.create(username='target')

    def get_target_url(self, target_user=None):
        if target_user is None:
            target_user = self.target_user
        response = self.client.get(reverse(
            "loginas-user-login", kwargs={'user_id': target_user.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlsplit(response['Location'])[2], "/")
        return response

    def assertCurrentUserIs(self, user):
        id_ = str(user.id if user is not None else None)
        self.assertEqual(self.client.get(reverse("current_user")).content, id_)

    def assertLoginError(self, resp):
        messages = CookieStorage(resp)._decode(resp.cookies['messages'].value)
        self.assertEqual([(m.level, m.message) for m in messages],
                         [(40, "You do not have permission to do that.")])

    def assertRaisesExact(self, exception, func, *args, **kwargs):
        try:
            func(*args, **kwargs)
            self.assertFail("{0} not raised".format(exc))
        except exception.__class__ as caught:
            self.assertEqual(caught.message, exception.message)

    def clear_cookies(self):
        for key in self.client.cookies.keys():
            del self.client.cookies[key]

    @override_settings(CAN_LOGIN_AS=login_as_nonstaff)
    def test_custom_permissions(self):
        user = create_user("user", "pass", is_superuser=False, is_staff=False)
        staff1 = create_user("staff", "pass", is_superuser=False, is_staff=True)
        staff2 = create_user("super", "pass", is_superuser=True, is_staff=True)

        # Regular user can't login as anyone
        self.assertTrue(self.client.login(username="user", password="pass"))
        self.assertLoginError(self.get_target_url())
        self.assertCurrentUserIs(user)
        self.clear_cookies()

        # Non-superuser staff user can login as regular user
        self.assertTrue(self.client.login(username="staff", password="pass"))
        response = self.get_target_url(user)
        self.assertNotIn('messages', response.cookies)
        self.assertCurrentUserIs(user)
        self.clear_cookies()

        # Non-superuser staff user cannot login as other staff
        self.assertTrue(self.client.login(username="staff", password="pass"))
        self.assertLoginError(self.get_target_url(staff2))
        self.assertCurrentUserIs(staff1)
        self.clear_cookies()

        # Superuser staff user can login as other staff
        self.assertTrue(self.client.login(username="super", password="pass"))
        response = self.get_target_url(staff1)
        self.assertNotIn('messages', response.cookies)
        self.assertCurrentUserIs(staff1)

    @override_settings(CAN_LOGIN_AS='loginas.tests.login_as_shorter_username')
    def test_custom_permissions_as_string(self):
        ray = create_user("ray", "pass")
        lonnie = create_user("lonnie", "pass")

        # Ray cannot login as Lonnie
        self.assertTrue(self.client.login(username="ray", password="pass"))
        self.assertLoginError(self.get_target_url(lonnie))
        self.assertCurrentUserIs(ray)
        self.clear_cookies()

        # Lonnie can login as Ray
        self.assertTrue(self.client.login(username="lonnie", password="pass"))
        response = self.get_target_url(ray)
        self.assertNotIn('messages', response.cookies)
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
        self.assertNotIn('messages', response.cookies)
        self.assertCurrentUserIs(self.target_user)

    def test_as_non_superuser(self):
        user = create_user("me", "pass", is_staff=True)
        self.assertTrue(self.client.login(username="me", password="pass"))
        self.assertLoginError(self.get_target_url())
        self.assertCurrentUserIs(user)

    def test_as_anonymous_user(self):
        self.assertLoginError(self.get_target_url())
        self.assertCurrentUserIs(None)
