from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth import views as auth_views
from django.contrib.auth.forms import SetPasswordForm
from django.contrib.auth.models import User
from django.core import mail
from django.urls import resolve, reverse
from django.test import TestCase


class PasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='tom', email='tom@dumy.com', password='asdf1234')
        self.uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        self.token = default_token_generator.make_token(user)
        self.url = reverse('accounts:password_reset_confirm', kwargs={
            'uidb64': self.uid, 'token': self.token})
        self.response = self.client.get(self.url, follow=True)

    def test_password_reset_confirm_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/reset/'+self.uid+'/'+self.token+'/', follow=True)
        self.assertEquals(response.status_code, 200)

    def test_password_reset_confirm_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_password_reset_confirm_view_function(self):
        view = resolve(self.url)
        self.assertEquals(view.func.view_class, auth_views.PasswordResetConfirmView)

    def test_password_reset_confirm_view_uses_correct_template(self):
        self.assertTemplateUsed(self.response, 'accounts/password_reset_confirm.html')

    def test_password_reset_confirm_view_uses_base_accounts_template(self):
        self.assertTemplateUsed(self.response, 'accounts/base_accounts.html')

    def test_password_reset_confirm_view_uses_base_template(self):
        self.assertTemplateUsed(self.response, 'base.html')

    def test_password_reset_confirm_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_password_reset_confirm_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SetPasswordForm)

    def test_password_reset_confirm_form_inputs(self):
        self.assertContains(self.response, '<input', 3)
        self.assertContains(self.response, 'type="password"', 2)


class InvalidPasswordResetConfirmTests(TestCase):
    def setUp(self):
        user = User.objects.create_user(username='tom', email='tom@dumy.com', password='asdf1234')
        uid = urlsafe_base64_encode(force_bytes(user.pk)).decode()
        token = default_token_generator.make_token(user)
        user.set_password('asdf1233')
        user.save()
        url = reverse('accounts:password_reset_confirm', kwargs={'uidb64': uid, 'token': token})
        self.response = self.client.get(url)

    def test_password_reset_confirm_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_password_reset_confirm_html(self):
        password_reset_url = reverse('accounts:password_reset')
        self.assertContains(self.response, 'invalid password reset link')
        self.assertContains(self.response, 'href="{0}"'.format(password_reset_url))
