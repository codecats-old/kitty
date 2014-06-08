from django.contrib import auth
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase, RequestFactory
from django.utils.importlib import import_module
from kitty import settings


class FiltersTestCase(TestCase):
    user = None

    def setUp(self):
        user = User()
        user.set_password('abc')
        user.username = 'test'
        user.email = 'test@t.t'
        user.save()
        self.user = user
        # self.user = auth.authenticate(username=user.username, password='abc')

    def authenticate(self):
        response = self.client.logout()
        self.assertFalse(response.request.user.is_authenticated())
        # self.client.login()
        # self.assertTrue(self.request.user.is_authenticated())
        # auth.logout(self.request)

    def test_access_denies_anonymous(self):
        self.client.logout()
        params = [
            {'frontsite:user': [{'id': '1'}]},
            {'frontsite:user': [{'id': '2'}]},
            {'frontsite:user': [{'id': '9998'}]},
            {'frontsite:user': [{'id': '9999'}]},
            {'frontsite:rhyme_detail': [{'id': '1'}, 'post']},
            {'frontsite:rhyme_detail': [{'id': '9999'}, 'post']}
        ]
        for item in params:
            url, kwargs = (item.keys()[0], item.values()[0])
            method = getattr(self.client, kwargs[1] if len(kwargs) == 2 else 'get')
            response = method(reverse(url, kwargs=kwargs[0]), follow=True)
            self.assertRedirects(response, reverse('frontsite:login'))