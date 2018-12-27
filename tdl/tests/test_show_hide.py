from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.test import TestCase

from ..models import Preferences
from ..views import show_hide


class PreferencesAuthenticatedUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='tommy', email='tommy@dumy.com', password='asdf1234')
        Preferences.objects.create(user=user, show_all=False)

    def setUp(self):
        self.client.login(username='tommy', password='asdf1234')

    def test_show_hide_url_exists_at_desired_location(self):
        response = self.client.get('/todolist/index/xhrvalt', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_show_hide_response_status_code_valid_value(self):
        url = reverse('tdl:show_hide', kwargs={'show': 'f'})
        response = self.client.get(url, follow=True)
        self.assertEquals(response.status_code, 200)

    def test_show_hide_url_resolves_view(self):
        view = resolve(reverse('tdl:show_hide', kwargs={'show': 'f'}))
        self.assertEquals(view.func, show_hide)

    def test_show_hide_redirection_login_required(self):
        self.client.logout()
        login_url = reverse('accounts:login')
        url = reverse('tdl:show_hide', kwargs={'show': 'f'})
        response = self.client.get(url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(
            login_url=login_url, url=url))


class PreferencesReturnedAsTheyChangeTestCases(TestCase):
    def test_show_hide_returns_correct_HttpResponse_case_False(self):
        user = User.objects.create_user(
            username='tommy', email='tommy@dumy.com', password='asdf1234')
        Preferences.objects.create(user=user, show_all=False)
        self.client.login(username='tommy', password='asdf1234')
        url = reverse('tdl:show_hide', kwargs={'show': 't'})
        response = self.client.get(url)
        self.assertEqual(response.content, b"True")

    def test_show_hide_returns_correct_HttpResponse_case_True(self):
        user = User.objects.create_user(
            username='tommy', email='tommy@dumy.com', password='asdf1234')
        Preferences.objects.create(user=user, show_all=True)
        self.client.login(username='tommy', password='asdf1234')
        url = reverse('tdl:show_hide', kwargs={'show': 'f'})
        response = self.client.get(url)
        self.assertEqual(response.content, b"False")
