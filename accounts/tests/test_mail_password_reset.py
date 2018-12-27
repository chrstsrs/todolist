from django.contrib.auth import views as auth_views
from django.core import mail
from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase


class PasswordResetMailTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='tom', email='tom@dumy.com', password='asdf1234')
        self.response = self.client.post(reverse('accounts:password_reset'), {
                                         'email': 'tom@dumy.com'})
        self.email = mail.outbox[0]

    def test_mail_password_reset_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/reset/')
        self.assertEquals(response.status_code, 200)

    def test_mail_password_reset_view_status_code(self):
        url = reverse('accounts:password_reset')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_mail_password_reset_view_uses_correct_template(self):
        response = self.client.get(reverse('accounts:password_reset'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/password_reset.html')

    def test_mail_password_reset_view_uses_base_accounts_template(self):
        response = self.client.get(reverse('accounts:password_reset'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'accounts/base_accounts.html')

    def test_mail_password_reset_view_uses_base_template(self):
        response = self.client.get(reverse('accounts:password_reset'), follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_mail_password_reset_url_resolves_mail_password_reset_view(self):
        view = resolve(reverse('accounts:password_reset'))
        self.assertEquals(view.func.view_class, auth_views.PasswordResetView)

    def test_email_subject(self):
        self.assertEqual('[To Do List] Reset your password !!!', self.email.subject)

    def test_email_body(self):
        context = self.response.context
        token = context.get('token')
        uid = context.get('uid')
        password_reset_token_url = reverse('accounts:password_reset_confirm', kwargs={
            'uidb64': uid,
            'token': token
        })
        self.assertIn(password_reset_token_url, self.email.body)
        self.assertIn('tom', self.email.body)
        self.assertIn('tom@dumy.com', self.email.body)

    def test_email_to(self):
        self.assertEqual(['tom@dumy.com', ], self.email.to)
