from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
import time
import os
from selenium import webdriver

from tdl.models import Task


class NewTaskTest(StaticLiveServerTestCase):
    def setUp(self):
        User.objects.create_user(username='tommy', email='tom@dumy.com', password='asdf4321')
        user = User.objects.first()
        Task.objects.create(name='Initial task', description='testing page', issued_by=user)

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

        # Login
        self.driver.get(self.get_url("home"))
        self.driver.find_element_by_name("username").send_keys("tommy")
        self.driver.find_element_by_name("password").send_keys("asdf4321")
        self.driver.find_element_by_id("submit_button").click()
        task = Task.objects.latest("issued_by")
        self.task_id = task.pk

    def tearDown(self):
        time.sleep(12)
        self.driver.quit()

    def get_url(self, namespace, **kwargs):
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        return self.live_server_url + reverse(namespace, **kwargs)

    def test_edit_task_title(self):
        # Opening the link we want to test
        self.driver.get(self.get_url("tdl:task_edit", kwargs={'task_id': self.task_id}))

        self.assertEqual("Edit the Task", self.driver.title)

    def test_incorrect_task_edit_empty_name(self):
        # Opening the link we want to test
        self.driver.get(self.get_url("tdl:task_edit", kwargs={'task_id': self.task_id}))

        # find the form element
        self.name = self.driver.find_element_by_id('id_name')
        self.description = self.driver.find_element_by_id('id_description')
        self.submit = self.driver.find_element_by_id("id_updateTask")

        # Fill the form with data
        self.name.clear()
        self.description.send_keys('... and an extra Description ...')

        # submitting the form
        self.submit.click()
        time.sleep(3)

        # check the returned result
        assert "This field is required." in self.driver.page_source

    def test_incorrect_task_edit_empty_description(self):
        # Opening the link we want to test
        self.driver.get(self.get_url("tdl:task_edit", kwargs={'task_id': self.task_id}))

        # find the form element
        self.name = self.driver.find_element_by_id('id_name')
        self.description = self.driver.find_element_by_id('id_description')
        self.submit = self.driver.find_element_by_id("id_updateTask")

        # Fill the form with data
        self.description.clear()

        # submitting the form
        self.submit.click()
        time.sleep(3)

        # check the returned result
        assert "This field is required." in self.driver.page_source

    def test_correct_task_edit(self):
        # Opening the link we want to test
        self.driver.get(self.get_url("tdl:task_edit", kwargs={'task_id': self.task_id}))

        # find the form element
        self.name = self.driver.find_element_by_id('id_name')
        self.description = self.driver.find_element_by_id('id_description')
        self.submit = self.driver.find_element_by_id("id_updateTask")

        # Fill the form with data
        self.name.clear()
        self.description.clear()
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

    def test_task_edit_link_to_task_list(self):
        # Opening the link we want to test
        self.driver.get(self.get_url("tdl:task_edit", kwargs={'task_id': self.task_id}))

        # find the form element
        self.name = self.driver.find_element_by_id('id_name')
        self.description = self.driver.find_element_by_id('id_description')
        self.index_link = self.driver.find_element_by_link_text('Tasks')
        self.submit = self.driver.find_element_by_id("id_updateTask")

        # Fill the form with data
        self.name.clear()
        self.description.clear()
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
