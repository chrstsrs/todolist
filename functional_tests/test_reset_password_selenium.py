from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
import time
import os
from selenium import webdriver


class ResetPasswordTest(StaticLiveServerTestCase):
    def setUp(self):
        User.objects.create_user(username='tommy', email='tom@dumy.com', password='asdf4321')
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

        # Opening the link we want to test
        self.driver.get(self.get_url("accounts:password_reset"))

        # find the form elements
        self.email = self.driver.find_element_by_id("id_email")
        self.submit = self.driver.find_element_by_id("submit_button")

    def tearDown(self):
        time.sleep(12)
        self.driver.quit()

    def get_url(self, namespace):
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        return self.live_server_url + reverse(namespace)

    def test_reset_password_title(self):
        self.assertEqual("Reset your password", self.driver.title)

    def test_email(self):
        # Fill the form with data
        self.email.send_keys("tom@dumy.com")

        # submitting the form
        self.submit.click()
        time.sleep(3)

        # check the returned result
        assert "Check your email for a link to reset your password." in self.driver.page_source
