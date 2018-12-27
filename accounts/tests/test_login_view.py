from django.contrib.auth import views as auth_views
from django.test import TestCase
from django.urls import reverse, resolve


class LoginIntoAccountTests(TestCase):
    def test_login_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_login_view_status_code(self):
        url = reverse('accounts:login')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_login_view_uses_correct_template(self):
        response = self.client.get(reverse('accounts:login'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_login_view_uses_base_accounts_template(self):
        response = self.client.get(reverse('accounts:login'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/base_accounts.html')

    def test_login_view_uses_base_template(self):
        response = self.client.get(reverse('accounts:login'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_login_url_resolves_login_view(self):
        view = resolve(reverse('accounts:login'))
        self.assertEquals(view.func.view_class, auth_views.LoginView)

    def test_login_contains_link_forget_password(self):
        login_url = reverse('accounts:login')
        password_reset_url = reverse('accounts:password_reset')
        response = self.client.get(login_url)
        self.assertContains(response, 'href="{0}"'.format(password_reset_url))

    def test_login_contains_link_signup(self):
        login_url = reverse('accounts:login')
        signup_url = reverse('accounts:signup')
        response = self.client.get(login_url)
        self.assertContains(response, 'href="{0}"'.format(signup_url))
