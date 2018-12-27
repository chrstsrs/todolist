from django.urls import reverse, resolve
from django.test import TestCase
from ..forms import SignUpForm


class SignUpFormTest(TestCase):
    def setUp(self):
        url = reverse('accounts:signup')
        self.response = self.client.get(url)

    def test_csrf(self):
        self.assertContains(self.response, 'csrfmiddlewaretoken')

    def test_contains_form(self):
        form = self.response.context.get('form')
        self.assertIsInstance(form, SignUpForm)

    def test_form_inputs(self):
        self.assertContains(self.response, '<input', 7)
        self.assertContains(self.response, 'type="text"', 2)
        self.assertContains(self.response, 'type="email"', 1)
        self.assertContains(self.response, 'type="password"', 2)
        self.assertContains(self.response, 'type="hidden"', 2)

    def test_form_signup_has_fields(self):
        form = SignUpForm()
        expected = ['username', 'email', 'password1', 'password2', 'captcha']
        actual = list(form.fields)
        self.assertSequenceEqual(expected, actual)

    def test_form_signup_task_field_email(self):
        form = SignUpForm()
        self.assertTrue(form.fields['email'].label == None or form.fields['email'].label == 'email')

    def test_form_signup_field_email_max_length(self):
        form = SignUpForm()
        self.assertEqual(form.fields['email'].max_length,  254)

    def test_form_signup_field_email_required(self):
        form = SignUpForm()
        self.assertEqual(form.fields['email'].required,  True)

    def test_form_signup_task_field_captcha(self):
        form = SignUpForm()
        self.assertTrue(form.fields['captcha'].label ==
                        None or form.fields['captcha'].label == 'captcha')
