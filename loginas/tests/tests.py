from urlparse import urlsplit

from django.test import TestCase
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.messages.storage.cookie import CookieStorage


def create_user(**kwargs):
    user = User(**kwargs)
    if 'password' in kwargs:
        user.set_password(kwargs['password'])
    user.save()
    return user


class ViewTest(TestCase):

    """Tests for user_login view"""

    def setUp(self):
        self.target_user = User.objects.create(username='target')

    def create_user(self, **kwargs):
        user = User(**kwargs)
        if 'password' in kwargs:
            user.set_password(kwargs['password'])
        user.save()
        return user

    def get_target_url(self):
        response = self.client.get(reverse(
            "loginas-user-login", kwargs={'user_id': self.target_user.id}))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(urlsplit(response['Location'])[2], "/")
        return response

    def assertCurrentUserIs(self, user):
        id_ = str(user.id if user is not None else None)
        self.assertEqual(self.client.get(reverse("current_user")).content, id_)

    def assertLoginError(self, resp):
        messages = CookieStorage(resp)._decode(resp.cookies['messages'].value)
        self.assertEqual([(m.level, m.message) for m in messages],
                         [(40, "You need to be a superuser to do that.")])

    def test_as_superuser(self):
        create_user(username="me", password="pass",
                         is_superuser=True, is_staff=True)
        self.assertTrue(self.client.login(username="me", password="pass"))
        response = self.get_target_url()
        self.assertNotIn('messages', response.cookies)
        self.assertCurrentUserIs(self.target_user)

    def test_as_non_superuser(self):
        user = create_user(username="me", password="pass", is_staff=True)
        self.assertTrue(self.client.login(username="me", password="pass"))
        self.assertLoginError(self.get_target_url())
        self.assertCurrentUserIs(user)

    def test_as_anonymous_user(self):
        self.assertLoginError(self.get_target_url())
        self.assertCurrentUserIs(None)
