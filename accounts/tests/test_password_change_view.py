from django.contrib.auth import views as auth_views
from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.test import TestCase


class PasswordChangeIntoAccountTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tom', email='tom@dumy.com', password='asdf1234')
        self.url = reverse('accounts:password_change')
        self.client.login(username='tom', password='asdf1234')

    def test_password_change_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/settings/password/')
        self.assertEquals(response.status_code, 200)

    def test_password_change_view_status_code(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_password_change_view_uses_correct_template(self):
        response = self.client.get(self.url)
        self.assertTemplateUsed(response, 'accounts/password_change.html')

    def test_password_change_view_uses_base_template(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_password_change_url_resolves_the_correct_view(self):
        view = resolve(self.url)
        self.assertEquals(view.func.view_class, auth_views.PasswordChangeView)


class LoginRequiredPasswordChangeTests(TestCase):
    def test_redirection(self):
        url = reverse('accounts:password_change')
        login_url = reverse('accounts:login')
        response = self.client.get(url)
        self.assertRedirects(response, f'{login_url}?next={url}')


class PasswordChangeTestCase(TestCase):
    def setUp(self, data={}):
        self.user = User.objects.create_user(
            username='tom', email='tom@dumy.com', password='asdf1234')
        self.url = reverse('accounts:password_change')
        self.client.login(username='tom', password='asdf1234')
        self.response = self.client.post(self.url, data)


class SuccessfulPasswordChangeTests(PasswordChangeTestCase):
    def setUp(self):
        super().setUp({
            'old_password': 'asdf1234',
            'new_password1': 'newasdf1234',
            'new_password2': 'newasdf1234',
        })

    def test_redirection(self):
        self.assertRedirects(self.response, reverse('accounts:password_change_done'))

    def test_password_changed(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('newasdf1234'))

    def test_user_authentication(self):
        response = self.client.get(reverse('tdl:index'))
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidPasswordChangeTests(PasswordChangeTestCase):
    def test_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_did_not_change_password(self):
        self.user.refresh_from_db()
        self.assertTrue(self.user.check_password('asdf1234'))
