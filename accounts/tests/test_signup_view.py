from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase
from ..views import signup
from ..forms import SignUpForm


class SignUpViewTests(TestCase):
    def setUp(self):
        url = reverse('accounts:signup')
        self.response = self.client.get(url)

    def test_signup_view_url_exists_at_desired_location(self):
        response = self.client.get('/accounts/signup/')
        self.assertEqual(response.status_code, 200)

    def test_signup_status_code(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_url_resolves_signup_view(self):
        view = resolve(reverse('accounts:signup'))
        self.assertEquals(view.func, signup)

    def test_signup_view_uses_correct_template(self):
        self.assertEqual(self.response.status_code, 200)
        self.assertTemplateUsed(self.response, 'accounts/signup.html')

    def test_password_reset_confirm_view_uses_base_accounts_template(self):
        self.assertTemplateUsed(self.response, 'accounts/base_accounts.html')

    def test_password_reset_confirm_view_uses_base_template(self):
        self.assertTemplateUsed(self.response, 'base.html')

    def test_signup_contains_link_login(self):
        login_url = reverse('accounts:login')
        signup_url = reverse('accounts:signup')
        response = self.client.get(signup_url)
        self.assertContains(response, 'href="{0}"'.format(login_url))


class SuccessfulSignUpTests(TestCase):
    def setUp(self):
        url = reverse('accounts:signup')
        data = {
            'username': 'tom',
            'email': 'tom@dummy.com',
            'password1': 'asdf4321',
            'password2': 'asdf4321',
            'captcha_0': 'anything',
            'captcha_1': 'PASSED'
        }
        self.response = self.client.post(url, data, follow=True)
        self.index_url = reverse('tdl:index')

    def test_signup_redirection(self):
        self.assertRedirects(self.response, self.index_url)

    def test_signup_user_creation(self):
        self.assertTrue(User.objects.exists())

    def test_signup_user_authentication(self):
        response = self.client.get(self.index_url, follow=True)
        user = response.context.get('user')
        self.assertTrue(user.is_authenticated)


class InvalidSignUpTests(TestCase):
    def setUp(self):
        url = reverse('accounts:signup')
        self.response = self.client.post(url, {})

    def test_signup_status_code_for_invalid_data(self):
        self.assertEquals(self.response.status_code, 200)

    def test_signup_form_errors(self):
        form = self.response.context.get('form')
        self.assertTrue(form.errors)

    def test_dont_create_user(self):
        self.assertFalse(User.objects.exists())
