from django.contrib.auth import views as auth_views
from django.test import TestCase
from django.urls import reverse, resolve


class PasswordResetDoneIntoAccountTests(TestCase):
    def test_password_reset_done_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/reset/done/')
        self.assertEquals(response.status_code, 200)

    def test_password_reset_done_view_status_code(self):
        url = reverse('accounts:password_reset_done')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_password_reset_done_view_uses_correct_template(self):
        response = self.client.get(reverse('accounts:password_reset_done'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset_done.html')

    def test_password_reset_done_view_uses_base_accounts_template(self):
        response = self.client.get(reverse('accounts:password_reset_done'), follow=True)
        self.assertTemplateUsed(response, 'accounts/base_accounts.html')

    def test_password_reset_done_view_uses_base_template(self):
        response = self.client.get(reverse('accounts:password_reset_done'), follow=True)
        self.assertTemplateUsed(response, 'base.html')

    def test_password_reset_done_url_resolves_the_correct_view(self):
        view = resolve(reverse('accounts:password_reset_done'))
        self.assertEquals(view.func.view_class, auth_views.PasswordResetDoneView)

    def test_password_reset_done_contains_link_login(self):
        password_reset_done_url = reverse('accounts:password_reset_done')
        login_url = reverse('accounts:login')
        response = self.client.get(password_reset_done_url)
        self.assertContains(response, 'href="{0}"'.format(login_url))
