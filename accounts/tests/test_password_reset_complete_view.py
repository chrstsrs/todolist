from django.test import TestCase
from django.urls import reverse, resolve
from django.contrib.auth import views as auth_views


class PasswordResetCompleteTests(TestCase):
    def setUp(self):
        url = reverse('accounts:password_reset_complete')
        self.response = self.client.get(url)

    def test_password_reset_complete_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/reset/complete/')
        self.assertEqual(response.status_code, 200)

    def test_password_reset_complete_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_password_reset_complete_resolves_view_function(self):
        view = resolve(reverse('accounts:password_reset_complete'))
        self.assertEquals(view.func.view_class, auth_views.PasswordResetCompleteView)

    def test_password_reset_complete_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'accounts/password_reset_complete.html')

    def test_password_reset_complete_view_uses_base_accounts_template(self):
        self.assertTemplateUsed(self.response, 'accounts/base_accounts.html')

    def test_password_reset_complete_view_uses_base_template(self):
        self.assertTemplateUsed(self.response, 'base.html')

    def test_password_reset_complete_contains_link_login(self):
        login_url = reverse('accounts:login')
        self.assertContains(self.response, 'href="{0}"'.format(login_url))

    def test_password_reset_complete_contains_link_home(self):
        home_url = reverse('home')
        self.assertContains(self.response, 'href="{0}"'.format(home_url))
