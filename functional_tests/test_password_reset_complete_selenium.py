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
        self.driver.get(self.get_url('accounts:password_reset_complete'))

        # find the link element
        self.login_link = self.driver.find_element_by_id("id_login_link")

    def tearDown(self):
        time.sleep(12)
        self.driver.quit()

    def get_url(self, namespace):
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        return self.live_server_url + reverse(namespace)

    def test_password_reset_complete_title(self):
        self.assertEqual("Password changed!", self.driver.title)

    def test_password_reset_complete_link_to_login(self):
        #  click the link
        self.login_link.click()
        time.sleep(3)

        # check the returned result
        self.assertEqual("ToDoList Login", self.driver.title)
