from django.contrib.staticfiles.testing import StaticLiveServerTestCase
from django.contrib.auth.models import User
from django.urls import reverse
import time
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from django.shortcuts import render, redirect, get_object_or_404

from tdl.models import Task, Preferences


class IndexTestTaskDoneIsTrueAndShowallIsFalse(StaticLiveServerTestCase):
    def setUp(self):
        User.objects.create_user(username='tommy', email='tom@dumy.com', password='asdf4321')
        self.user = User.objects.first()
        Task.objects.create(name='This task has been Done',
                            description='testing page', issued_by=self.user, done=True, done_by=self.user)

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

        # Opening the link we want to test
        # self.driver.get(self.get_url("tdl:index"))

        # Login
        self.driver.get(self.get_url("home"))
        self.driver.find_element_by_name("username").send_keys("tommy")
        self.driver.find_element_by_name("password").send_keys("asdf4321")
        self.driver.find_element_by_id("submit_button").click()

    def tearDown(self):
        time.sleep(12)
        self.driver.quit()

    def get_url(self, namespace, **kwargs):
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        return self.live_server_url + reverse(namespace, **kwargs)

    def test_index_task_title(self):
        self.assertEqual("To Do List", self.driver.title)

    def test_index_can_access_the_new_task(self):
        # find the element
        button = self.driver.find_element_by_id('id_newTask')

        # submitting the form
        button.click()
        time.sleep(3)

        # check the returned result
        self.assertEqual("Issue a New Task", self.driver.title)

    def test_index_Show_all_Tasks(self):
        # find the form element
        self.show_hide = self.driver.find_element_by_id('taskFilter')
        wait = WebDriverWait(self.driver, 10)
        self.assertTrue(wait.until(EC.text_to_be_present_in_element(
            (By.ID, 'taskFilter'), 'Show Completed tasks')))
        self.assertTrue(wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "doneclass"))))

        # submitting the form
        self.show_hide.click()
        time.sleep(3)

        self.assertTrue(wait.until(EC.text_to_be_present_in_element(
            (By.ID, 'taskFilter'), 'Hide Completed tasks')))
        self.assertTrue(wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "doneclass"))))


class IndexTestTaskDoneIsTrueAndShowallIsTrue(StaticLiveServerTestCase):
    def setUp(self):
        User.objects.create_user(username='tommy', email='tom@dumy.com', password='asdf4321')
        self.user = User.objects.first()
        Task.objects.create(name='This is a task',
                            description='testing page', issued_by=self.user, done=True, done_by=self.user)
        Preferences.objects.filter(user=self.user).update(show_all=True)

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

        # Opening the link we want to test
        # self.driver.get(self.get_url("tdl:index"))

        # Login
        self.driver.get(self.get_url("home"))
        self.driver.find_element_by_name("username").send_keys("tommy")
        self.driver.find_element_by_name("password").send_keys("asdf4321")
        self.driver.find_element_by_id("submit_button").click()

    def tearDown(self):
        time.sleep(12)
        self.driver.quit()

    def get_url(self, namespace, **kwargs):
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        return self.live_server_url + reverse(namespace, **kwargs)

    def test_index_hide_done_Tasks(self):
        # find the form element
        self.show_hide = self.driver.find_element_by_id('taskFilter')
        wait = WebDriverWait(self.driver, 10)
        self.assertTrue(wait.until(EC.text_to_be_present_in_element(
            (By.ID, 'taskFilter'), 'Hide Completed tasks')))
        self.assertTrue(wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, "doneclass"))))

        # submitting the form
        self.show_hide.click()
        time.sleep(3)

        # check the returned result
        self.assertTrue(wait.until(EC.text_to_be_present_in_element(
            (By.ID, 'taskFilter'), 'Show Completed tasks')))
        self.assertTrue(wait.until(
            EC.invisibility_of_element_located((By.CLASS_NAME, "doneclass"))))
        time.sleep(2)

    def test_index_edit_button(self):
        # find the edit button
        time.sleep(3)
        self.button = self.driver.find_element(
            By.XPATH, "//tr[@class='doneclass'][1]/td[1]/a[@class='btn btn-primary btn-sm'][1]")

        # click it
        self.button.click()
        time.sleep(3)

        # check the returned result
        self.assertEqual("Edit the Task", self.driver.title)

    def test_index_undone_button(self):
        # find the undone button
        time.sleep(3)
        self.button = self.driver.find_element(
            By.XPATH, "//tr[@class='doneclass'][1]/td[@class='align-middle'][2]/a[@class='btn btn-primary btn-sm'][1]")

        # click it
        self.button.click()

        # check the returned result
        try:
            self.button = self.driver.find_element(
                By.XPATH, "//tr[@class='doneclass'][1]/td[@class='align-middle'][2]/a[@class='btn btn-primary btn-sm'][1]")
        except NoSuchElementException:
            True
        else:
            False
        time.sleep(2)

    def test_index_undone_button_yields_message_for_the_last_who_worked_on_that_task(self):
        # find the undone button
        time.sleep(3)
        self.button = self.driver.find_element(
            By.XPATH, "//tr[@class='doneclass'][1]/td[@class='align-middle'][2]/a[@class='btn btn-primary btn-sm'][1]")

        # click it
        self.button.click()
        time.sleep(3)

        # check the returned result
        assert 'tommy has worked last' in self.driver.page_source

    def test_index_delete_button(self):
        # find the delete button
        self.button = self.driver.find_element(
            By.XPATH, "//tr[@class='doneclass'][1]/td[@class='align-middle'][1]/a[@class='btn btn-primary btn-sm'][1]")
        assert 'This is a task' in self.driver.page_source

        # click it
        self.button.click()
        time.sleep(3)

        # check the returned result
        assert 'This is a task' in self.driver.page_source

        # find the confirm button
        self.confirm = self.driver.find_element_by_id('id_deleteTask')

        # click it
        self.confirm.click()
        time.sleep(3)

        # check the returned result
        assert 'This is a task' not in self.driver.page_source


class IndexTestDefaultDoneIsFalse(StaticLiveServerTestCase):
    def setUp(self):
        User.objects.create_user(username='tommy', email='tom@dumy.com', password='asdf4321')
        self.user = User.objects.first()
        Task.objects.create(name='This is a task',
                            description='testing page', issued_by=self.user, done=False, done_by=self.user)

        self.driver = webdriver.Firefox()
        self.driver.implicitly_wait(5)
        self.driver.maximize_window()

        # Opening the link we want to test
        # self.driver.get(self.get_url("tdl:index"))

        # Login
        self.driver.get(self.get_url("home"))
        self.driver.find_element_by_name("username").send_keys("tommy")
        self.driver.find_element_by_name("password").send_keys("asdf4321")
        self.driver.find_element_by_id("submit_button").click()

    def tearDown(self):
        time.sleep(12)
        self.driver.quit()

    def get_url(self, namespace, **kwargs):
        staging_server = os.environ.get('STAGING_SERVER')
        if staging_server:
            self.live_server_url = 'http://' + staging_server
        return self.live_server_url + reverse(namespace, **kwargs)

    def test_index_done_button(self):
        # find the done button
        time.sleep(3)
        self.button = self.driver.find_element_by_name('done_undone')
        assert "Done?" in self.driver.page_source

        # click it
        self.button.click()
        time.sleep(3)

        # check the returned result
        assert "Done?" not in self.driver.page_source
