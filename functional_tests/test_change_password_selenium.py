from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
import time
import os
from selenium import webdriver


class ChangePasswordTest(StaticLiveServerTestCase):
    def setUp(self):
        User.objects.create_user(username='tommy', email='tom@dumy.com', password='asdf4321')
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

        # Opening the link we want to test
        self.driver.get(self.get_url("accounts:password_change"))

        # ... after Login ...
        self.driver.find_element_by_name("username").send_keys("tommy")
        self.driver.find_element_by_name("password").send_keys("asdf4321")
        self.driver.find_element_by_id("submit_button").click()

        # find the form elements
        self.old_password = self.driver.find_element_by_id("id_old_password")
        self.password1 = self.driver.find_element_by_id("id_new_password1")
        self.password2 = self.driver.find_element_by_id("id_new_password2")
        self.submit = self.driver.find_element_by_id("submit_button")

    def tearDown(self):
        time.sleep(12)
        self.driver.quit()

    def get_url(self, namespace):
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        return self.live_server_url + reverse(namespace)

    def test_change_password_title(self):
        self.assertEqual("Change password", self.driver.title)

    def test_incorrect_old_password(self):
        # Fill the form with data
        self.old_password.send_keys("asdffdg4321")
        self.password1.send_keys("asdfg54321")
        self.password2.send_keys("asdfg54321")

        # submitting the form
        self.submit.click()
        time.sleep(3)

        # check the returned result
        assert 'Your old password was entered incorrectly. Please enter it again.' in self.driver.page_source

    def test_unmatched_new_password(self):
        # Fill the form with data
        self.old_password.send_keys("asdf4321")
        self.password1.send_keys("asdfg54321")
        self.password2.send_keys("asdfg5432111111")

        # submitting the form
        self.submit.click()
        time.sleep(3)

        # check the returned result
        assert "The two password fields didn't match." in self.driver.page_source

    def test_correct_new_password(self):
        # Fill the form with data
        self.old_password.send_keys("asdf4321")
        self.password1.send_keys("asdf432123")
        self.password2.send_keys("asdf432123")

        # submitting the form
        self.submit.click()
        time.sleep(3)

        # check the returned result
        self.assertEqual("Change password successful", self.driver.title)
