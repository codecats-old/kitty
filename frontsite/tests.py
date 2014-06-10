from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test import TestCase


class AccessTestCase(TestCase):
    user = None

    def setUp(self):
        user = User()
        user.set_password('abc')
        user.username = 'test'
        user.email = 'test@t.t'
        user.save()
        self.user = user

    def test_approve_authenticated(self):
        response = self.client.logout()
        self.client.login(username=self.user.username, password='abc')

        params = [
            {'frontsite:user': [{'id': self.user.id}, 'get']},
            {'frontsite:category': [{}, 'post']}
        ]

        for item in params:
            url, kwargs = (item.keys()[0], item.values()[0])
            method = getattr(self.client, kwargs[1] if len(kwargs) == 2 else 'get')
            response = method(reverse(url, kwargs=kwargs[0]), follow=True)
            self.assertEquals(response.status_code, 200)

    def test_denies_anonymous(self):
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