from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.models import User
from django.urls import reverse
import time
import os
from selenium import webdriver


class PasswordResetConfirmTest(StaticLiveServerTestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='tommy', email='tom@dumy.com', password='asdf4321')
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk)).decode()
        self.token = default_token_generator.make_token(self.user)

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

        # Opening the link we want to test
        self.driver.get(self.get_url('accounts:password_reset_confirm', kwargs={
            'uidb64': self.uid, 'token': self.token}))

       # find the form elements
        self.password1 = self.driver.find_element_by_id("id_new_password1")
        self.password2 = self.driver.find_element_by_id("id_new_password2")
        self.submit_button = self.driver.find_element_by_id("submit_button")

    def tearDown(self):
        time.sleep(12)
        self.driver.quit()

    def get_url(self, namespace, **kwargs):
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        return self.live_server_url + reverse(namespace, **kwargs)

    def test_password_reset_confirm_title(self):
        self.assertEqual("Change password for " + self.user.username, self.driver.title)

    def test_password_reset_confirm_invalid_new_password_unmatched_case(self):
        # Fill the form with data
        self.password1.send_keys("asdfgh654321")
        self.password2.send_keys("aaaaasdf4444")

        # submitting the form
        self.submit_button.click()
        time.sleep(3)

        # check the returned result
        assert "The two password fields didn't match." in self.driver.page_source

    def test_password_reset_confirm_invalid_new_password_empty_field_case(self):
        # Fill the form with data
        self.password1.send_keys("asdfgh654321")
        self.password2.send_keys("")

        # submitting the form
        self.submit_button.click()
        time.sleep(3)

        # check the returned result
        assert "This field is required." in self.driver.page_source

    def test_password_reset_confirm_invalid_new_password_too_common_case(self):
        # Fill the form with data
        self.password1.send_keys("asdf1234")
        self.password2.send_keys("asdf1234")

        # submitting the form
        self.submit_button.click()
        time.sleep(3)

        # check the returned result
        assert "This password is too common." in self.driver.page_source

    def test_password_reset_confirm_invalid_new_password_entirely_numeric_case(self):
        # Fill the form with data
        self.password1.send_keys("3457621960")
        self.password2.send_keys("3457621960")

        # submitting the form
        self.submit_button.click()
        time.sleep(3)

        # check the returned result
        assert "This password is entirely numeric." in self.driver.page_source

    def test_password_reset_confirm_valid_new_password(self):
        # Fill the form with data
        self.password1.send_keys("asdfg54321")
        self.password2.send_keys("asdfg54321")

        # submitting the form
        self.submit_button.click()
        time.sleep(3)

        # check the returned result
        self.assertEqual("Password changed!", self.driver.title)
