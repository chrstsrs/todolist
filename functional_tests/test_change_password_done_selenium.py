from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
import time
import os
from selenium import webdriver


class ChangePasswordDoneTest(StaticLiveServerTestCase):
    def setUp(self):
        User.objects.create_user(username='tommy', email='tom@dumy.com', password='asdf4321')
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

        # Opening the link we want to test
        self.driver.get(self.get_url("accounts:password_change_done"))

        # ... after Login ...
        self.driver.find_element_by_name("username").send_keys("tommy")
        self.driver.find_element_by_name("password").send_keys("asdf4321")
        self.driver.find_element_by_id("submit_button").click()

        # find the element
        self.return_to_home = self.driver.find_element_by_id("return_to_home_id")
        self.change_pasword = self.driver.find_element_by_id("change_pasword_id")

    def tearDown(self):
        time.sleep(12)
        self.driver.quit()

    def get_url(self, namespace):
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        return self.live_server_url + reverse(namespace)

    def test_change_password_done_title(self):
        self.assertEqual("Change password successful", self.driver.title)

    def test_change_password_done_link_to_home(self):
        # click it
        self.return_to_home.click()
        time.sleep(3)

        # check the returned result
        self.assertEqual("To Do List", self.driver.title)

    def test_change_password_done_link_to_change_password(self):
        # click it
        self.change_pasword.click()
        time.sleep(3)

        # check the returned result
        self.assertEqual("Change password", self.driver.title)
