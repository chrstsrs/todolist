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
        self.driver.get(self.get_url("accounts:password_reset_done"))

        # find the form elements
        self.return_to_login = self.driver.find_element_by_id("return_to_login_id")

    def tearDown(self):
        time.sleep(12)
        self.driver.quit()

    def get_url(self, namespace, **kwargs):
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        return self.live_server_url + reverse(namespace, **kwargs)

    def test_reset_password_title(self):
        self.assertEqual("Reset your password", self.driver.title)

    def test_reset_password_done_link_to_login(self):
        # click the link
        self.return_to_login.click()
        time.sleep(3)

        # check the returned result
        self.assertEqual("ToDoList Login", self.driver.title)
