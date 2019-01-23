from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.test import TestCase


class PasswordChangeDoneIntoAccountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tom', email='tom@dumy.com', password='asdf1234')
        self.client.login(username='tom', password='asdf1234')

    def test_password_change_done_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/settings/password/done/')
        self.assertEquals(response.status_code, 200)

    def test_password_change_done_view_status_code(self):
        url = reverse('accounts:password_change_done')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_password_change_done_view_uses_correct_template(self):
        response = self.client.get(reverse('accounts:password_change_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_change_done.html')

    def test_password_change_done_view_uses_base_template(self):
        response = self.client.get(reverse('accounts:password_change_done'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_password_change_done_url_resolves_the_correct_view(self):
        view = resolve(reverse('accounts:password_change_done'))
        self.assertEquals(view.func.view_class, auth_views.PasswordChangeDoneView)

    def test_password_change_done_contains_link_home(self):
        password_change_done_url = reverse('accounts:password_change_done')
        home_url = reverse('home')
        response = self.client.get(password_change_done_url)
        self.assertContains(response, 'href="{0}"'.format(home_url))

    def test_password_change_done_contains_link_password_change(self):
        password_change_done_url = reverse('accounts:password_change_done')
        password_change_url = reverse('accounts:password_change')
        response = self.client.get(password_change_done_url)
        self.assertContains(response, 'href="{0}"'.format(password_change_url))


class LoginRequiredPasswordChangeTests(TestCase):
    def test_password_change_done_redirection(self):
        url = reverse('accounts:password_change_done')
        login_url = reverse('accounts:login')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')
