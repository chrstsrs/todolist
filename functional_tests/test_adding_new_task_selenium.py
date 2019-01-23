from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
import time
import os
from selenium import webdriver


class NewTaskTest(StaticLiveServerTestCase):
    def setUp(self):
        User.objects.create_user(username='tommy', email='tom@dumy.com', password='asdf4321')
        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

        # Opening the link we want to test
        self.driver.get(self.get_url("tdl:new_task"))

        # Login
        self.driver.find_element_by_name("username").send_keys("tommy")
        self.driver.find_element_by_name("password").send_keys("asdf4321")
        self.driver.find_element_by_id("submit_button").click()

        # find the form element
        self.name = self.driver.find_element_by_id('id_name')
        self.description = self.driver.find_element_by_id('id_description')
        self.index_link = self.driver.find_element_by_link_text('Tasks')
        self.submit = self.driver.find_element_by_id("id_postNewTask")

    def tearDown(self):
        time.sleep(12)
        self.driver.quit()

    def get_url(self, namespace):
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        return self.live_server_url + reverse(namespace)

    def test_new_task_title(self):
        self.assertEqual("Issue a New Task", self.driver.title)

    def test_incorrect_new_task_empty_name(self):
        # Fill the form with data
        self.name.send_keys('')
        self.description.send_keys('Just a Description')

        # submitting the form
        self.submit.click()
        time.sleep(3)

        # check the returned result
        assert "This field is required." in self.driver.page_source

    def test_incorrect_new_task_empty_description(self):
        # Fill the form with data
        self.name.send_keys('A new task')
        self.description.send_keys('')

        # submitting the form
        self.submit.click()
        time.sleep(3)

        # check the returned result
        assert "This field is required." in self.driver.page_source

    def test_correct_new_task(self):
        # Fill the form with data
        self.name.send_keys('A new task')
        self.description.send_keys('Just a Description')

        # submitting the form
        self.submit.click()
        time.sleep(3)

        # check the returned result
        assert "Issued by" in self.driver.page_source
        self.assertEqual("To Do List", self.driver.title)
        assert 'A new task' in self.driver.page_source
        assert 'Just a Description' in self.driver.page_source
        assert 'tommy' in self.driver.page_source

    def test_link_to_task_list(self):
        # Fill the form with data
        self.name.send_keys('A new task')
        self.description.send_keys('Just a Description')

        # click to the index page
        self.index_link.click()
        time.sleep(3)

        # check the returned result
        assert "Issued by" in self.driver.page_source
        self.assertEqual("To Do List", self.driver.title)
        assert 'A new task' not in self.driver.page_source
        assert 'Just a Description' not in self.driver.page_source
