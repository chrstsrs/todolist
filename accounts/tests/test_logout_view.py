from django.contrib.auth import views as auth_views
from django.test import TestCase
from django.urls import reverse, resolve


class LogoutIntoAccountTests(TestCase):
    def test_logout_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/logout/')
        self.assertRedirects(response, reverse('home'), status_code=302, target_status_code=302)

    def test_logout_view_status_code(self):
        url = reverse('accounts:logout')
        response = self.client.get(url, follow=True)
        self.assertEquals(response.status_code, 200)

    def test_logout_view_uses_correct_template(self):
        response = self.client.get(reverse('accounts:logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_logout_view_uses_base_accounts_template(self):
        response = self.client.get(reverse('accounts:logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/base_accounts.html')

    def test_logout_view_uses_base_template(self):
        response = self.client.get(reverse('accounts:logout'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_logout_url_resolves_logout_view(self):
        view = resolve(reverse('accounts:logout'))
        self.assertEquals(view.func.view_class, auth_views.LogoutView)

    def test_logout_redirects_login(self):
        logout_url = reverse('accounts:logout')
        response = self.client.get(logout_url, follow=True)
        login_url = reverse('accounts:login')
        url = reverse('tdl:index')
        self.assertRedirects(response, f'{login_url}?next={url}')
