from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.auth.models import User
from django.core import mail
from django.urls import resolve, reverse
from django.test import TestCase


class PasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('accounts:password_reset')
        self.response = self.client.get(url)

    def test_password_reset_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/reset/')
        self.assertEquals(response.status_code, 200)

    def test_password_reset_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_password_reset_resolves_view_function(self):
        view = resolve(reverse('accounts:password_reset'))
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)

    def test_password_reset_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_password_reset_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'accounts/password_reset.html')

    def test_password_reset_view_uses_base_accounts_template(self):
        self.assertTemplateUsed(self.response, 'accounts/base_accounts.html')

    def test_password_reset_view_uses_base_template(self):
        self.assertTemplateUsed(self.response, 'base.html')

    def test_password_reset_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, PasswordResetForm)

    def test_password_reset_form_inputs(self):
        self.assertContains(self.response, '<input', 2)
        self.assertContains(self.response, 'type="email"', 1)


class SuccessfulPasswordResetTests(TestCase):
    def setUp(self):
        email = 'tom@dumy.com'
        User.objects.create_user(username='tom', email=email, password='asdf1234')
        url = reverse('accounts:password_reset')
        self.response = self.client.post(url, {'email': email})

    def test_password_reset_redirection(self):
        url = reverse('accounts:password_reset_done')
        self.assertRedirects(self.response, url)

    def test_password_reset_send_email(self):
        self.assertEqual(1, len(mail.outbox))


class InvalidPasswordResetTests(TestCase):
    def setUp(self):
        url = reverse('accounts:password_reset')
        self.response = self.client.post(url, {'email': 'tomdoesnotexist@dumy.com'})

    def test_password_reset_redirection(self):
        url = reverse('accounts:password_reset_done')
        self.assertRedirects(self.response, url)

    def test_password_reset_no_reset_email_sent(self):
        self.assertEqual(0, len(mail.outbox))
