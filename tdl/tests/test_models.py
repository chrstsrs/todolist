from django.contrib.auth.models import User
from django.test import TestCase

from ..models import Task, Preferences


class TaskModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='tom', email='tom@dummy.com', password='asdf1234')

    def setUp(self):
        self.client.login(username='tom', password='asdf1234')
        user = User.objects.first()
        Task.objects.create(
            name='another task', description='testing page', issued_by=user)

    def test_field_label_name(self):
        task = Task.objects.first()
        field_label = task._meta.get_field('name').verbose_name
        self.assertEquals(field_label, 'name')

    def test_field_label_description(self):
        task = Task.objects.first()
        field_label = task._meta.get_field('description').verbose_name
        self.assertEquals(field_label, 'description')

    def test_field_label_issued_by(self):
        task = Task.objects.first()
        field_label = task._meta.get_field('issued_by').verbose_name
        self.assertEquals(field_label, 'issued by')

    def test_field_label_done(self):
        task = Task.objects.first()
        field_label = task._meta.get_field('done').verbose_name
        self.assertEquals(field_label, 'done')

    def test_field_label_done_by(self):
        task = Task.objects.first()
        field_label = task._meta.get_field('done_by').verbose_name
        self.assertEquals(field_label, 'done by')

    def test_field_label_name_max_length(self):
        task = Task.objects.first()
        field_length = task._meta.get_field('name').max_length
        self.assertEquals(field_length, 40)

    def test_field_label_description_max_length(self):
        task = Task.objects.first()
        field_length = task._meta.get_field('description').max_length
        self.assertEquals(field_length, 4000)


class PreferencesModelTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='tom', email='tom@dummy.com', password='asdf1234')
        user = User.objects.first()
        Preferences.objects.create(user=user, show_all=False)

    def test_field_label_user(self):
        preferences = Preferences.objects.first()
        field_label = preferences._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')

    def test_field_label_show_all(self):
        preferences = Preferences.objects.first()
        field_label = preferences._meta.get_field('show_all').verbose_name
        self.assertEquals(field_label, 'show all')
