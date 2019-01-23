from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
import time
import os
from django.urls import reverse
from selenium import webdriver


class SignupTest(StaticLiveServerTestCase):
    def setUp(self):
        User.objects.create_user(username='tommy', email='tom@dumy.com', password='asdf4321')
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

        # Opening the link we want to test
        self.driver.get(self.get_url("accounts:signup"))

        # find the form element
        self.first_name = self.driver.find_element_by_name('username')
        self.email = self.driver.find_element_by_name('email')
        self.password1 = self.driver.find_element_by_name('password1')
        self.password2 = self.driver.find_element_by_name('password2')
        self.captcha1 = self.driver.find_element_by_id("id_captcha_1")
        self.submit = self.driver.find_element_by_id("submit_button")

    def tearDown(self):
        time.sleep(12)
        self.driver.quit()

    def get_url(self, namespace):
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        return self.live_server_url + reverse(namespace)

    def test_incorrect_signup_different_passwords(self):
        # Fill the form with data
        self.first_name.send_keys('charis2')
        self.email.send_keys('charis2@qawba.com')
        self.password1.send_keys('asdf4321')
        self.password2.send_keys('aaaa4321')
        self.captcha1.send_keys('PASSED')

        # submitting the form
        self.submit.click()
        time.sleep(3)

        # check the returned result
        assert "The two password fields didn't match" in self.driver.page_source

    def test_incorrect_signup_empty_email(self):
        # Fill the form with data
        self.first_name.send_keys('charis2')
        self.email.send_keys('')
        self.password1.send_keys('asdf4321')
        self.password2.send_keys('aaaa4321')
        self.captcha1.send_keys('PASSED')

        # submitting the form
        self.submit.click()
        time.sleep(3)

        # check the returned result
        assert "This field is required" in self.driver.page_source

    def test_incorrect_signup_invalid_email(self):
        # Fill the form with data
        self.first_name.send_keys('charis2')
        self.email.send_keys('charis2')
        self.password1.send_keys('asdf4321')
        self.password2.send_keys('aaaa4321')
        self.captcha1.send_keys('PASSED')

        # submitting the form
        self.submit.click()
        time.sleep(3)

        # check the returned result
        assert "Enter a valid email address" in self.driver.page_source

    def test_incorrect_signup_short_password(self):
        # Fill the form with data
        self.first_name.send_keys('charis222')
        self.email.send_keys('charis222@qawba.com')
        self.password1.send_keys('asdf')
        self.password2.send_keys('asdf')
        self.captcha1.send_keys('PASSED')

        # submitting the form
        self.submit.click()
        time.sleep(3)

        # check the returned result
        assert "This password is too short" in self.driver.page_source

    def test_incorrect_signup_common_password(self):
        # Fill the form with data
        self.first_name.send_keys('charis2')
        self.email.send_keys('charis2@qawba.com')
        self.password1.send_keys('password1')
        self.password2.send_keys('password1')
        self.captcha1.send_keys('PASSED')

        # submitting the form
        self.submit.click()
        time.sleep(3)

        # check the returned result
        assert "This password is too common" in self.driver.page_source

    def test_incorrect_signup_only_numeric_password(self):
        # Fill the form with data
        self.first_name.send_keys('charis2')
        self.email.send_keys('charis2@qawba.com')
        self.password1.send_keys('123456789')
        self.password2.send_keys('123456789')
        self.captcha1.send_keys('PASSED')

        # submitting the form
        self.submit.click()
        time.sleep(3)

        # check the returned result
        assert "This password is entirely numeric." in self.driver.page_source

    def test_incorrect_signup_with_same_username(self):
        # Fill the form with data
        self.first_name.send_keys('tommy')
        self.email.send_keys('tommy@dumy.com')
        self.password1.send_keys('asdf4321')
        self.password2.send_keys('asdf4321')
        self.captcha1.send_keys('PASSED')

        # submitting the form
        self.submit.click()
        time.sleep(3)

        # check the returned result
        assert "A user with that username already exists." in self.driver.page_source

    def test_correct_signup(self):
        # Fill the form with data
        self.first_name.send_keys('charis2234')
        self.email.send_keys('charis22@qawba.com')
        self.password1.send_keys('asdf4321')
        self.password2.send_keys('asdf4321')
        self.captcha1.send_keys('PASSED')

        # submitting the form
        self.submit.click()
        time.sleep(3)

        # check the returned result
        assert 'Description' in self.driver.page_source
