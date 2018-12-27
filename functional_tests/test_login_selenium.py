from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
import time
import os
from selenium import webdriver


class LoginTest(StaticLiveServerTestCase):
    def setUp(self):
        User.objects.create_user(username='tommy', email='tom@dumy.com', password='asdf4321')
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(10)
        self.driver.maximize_window()

        # Opening the link we want to test
        self.driver.get(self.get_url("home"))

    def tearDown(self):
        time.sleep(12)
        self.driver.quit()

    def get_url(self, namespace):
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        return self.live_server_url + reverse(namespace)

    def test_login_title(self):
        self.assertEqual("ToDoList Login", self.driver.title)

    def test_incorrect_login(self):
        # find the form elements
        self.field_username = self.driver.find_element_by_name("username")
        self.field_passwd = self.driver.find_element_by_name("password")
        self.submit = self.driver.find_element_by_id("submit_button")

        # Fill the form with data
        self.field_username.send_keys("tommy")
        self.field_passwd.send_keys("asdffdg4321")

        # submitting the form
        self.submit.click()
        time.sleep(3)

        # check the returned result
        assert 'Please enter a correct username and password.' in self.driver.page_source
        self.driver.implicitly_wait(10)

    def test_correct_login(self):
        # find the form elements
        self.field_username = self.driver.find_element_by_name("username")
        self.field_passwd = self.driver.find_element_by_name("password")
        self.submit = self.driver.find_element_by_id("submit_button")

        # Fill the form with data
        self.field_username.send_keys("tommy")
        self.field_passwd.send_keys("asdf4321")

        # submitting the form
        self.submit.click()
        time.sleep(3)

        # check the returned result
        assert 'Description' in self.driver.page_source
