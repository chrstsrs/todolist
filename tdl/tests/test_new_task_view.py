from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase, Client
from ..views import index, new_task
from ..models import Task
from ..forms import NewTaskForm


class NewTaskTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='tommy', email='tom@dumy.com', password='asdf1234')

    def setUp(self):
        self.client.login(username='tommy', password='asdf1234')
        self.user = User.objects.first()
        Task.objects.create(name='another task', description='testing page', issued_by=self.user)

    def test_new_task_view_url_exists_at_desired_location(self):
        response = self.client.get('/todolist/new/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_new_view_status_code(self):
        url = reverse('tdl:new_task')
        response = self.client.get(url, follow=True)
        self.assertEquals(response.status_code, 200)

    def test_new_task_view_uses_correct_template(self):
        response = self.client.get(reverse('tdl:new_task'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tdl/new_task.html')

    def test_new_task_view_uses_base_template(self):
        response = self.client.get(reverse('tdl:new_task'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_new_url_resolves_new_view(self):
        view = resolve(reverse('tdl:new_task'))
        self.assertEquals(view.func, new_task)

    def test_new_task_view_contains_link_to_index_view(self):
        new_url = reverse('tdl:new_task')
        index_url = reverse('tdl:index')
        response = self.client.get(new_url, follow=True)
        self.assertContains(response, 'href="{0}"'.format(index_url))

    def test_csrf(self):
        url = reverse('tdl:new_task')
        response = self.client.get(url, follow=True)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_new_task_valid_task_data(self):
        url = reverse('tdl:new_task')
        data = {
            'name': 'task2',
            'description': 'Testing data',
            'issued_by': self.user
        }
        response = self.client.post(url, data, follow=True)
        query = Task.objects.values()[1]
        self.assertEquals(data['name'], query['name'])
        self.assertEquals(data['description'], query['description'])
        self.assertEquals(query['issued_by_id'], 1)

    def test_new_task_invalid_data(self):
        url = reverse('tdl:new_task')
        response = self.client.post(url, {}, follow=True)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_task_invalid_data_empty_fields(self):
        url = reverse('tdl:new_task')
        data = {
            'name': "",
            'description': "",
            'issued_by': ""
        }
        response = self.client.post(url, {}, follow=True)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_new_task_contains_form(self):
        url = reverse('tdl:new_task')
        response = self.client.get(url, follow=True)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTaskForm)

    def test_index_contains_link_for_password_change(self):
        password_url = reverse('accounts:password_change')
        url = reverse('tdl:new_task')
        response = self.client.get(url, follow=True)
        self.assertContains(response, 'href="{0}"'.format(password_url))

    def test_index_contains_link_for_logout(self):
        logout_url = reverse('accounts:logout')
        url = reverse('tdl:new_task')
        response = self.client.get(url, follow=True)
        self.assertContains(response, 'href="{0}"'.format(logout_url))


class LoginRequiredNewTaskTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='tommy', email='tom@dumy.com', password='asdf1234')
        self.client.login(username='tommy', password='asdf1234')
        user = User.objects.first()
        self.client.logout()
        self.url = reverse('tdl:new_task')
        self.response = self.client.get(self.url)

    def test_login_redirection_for_new_task(self):
        login_url = reverse('accounts:login')
        self.assertRedirects(self.response, '{login_url}?next={url}'.format(
            login_url=login_url, url=self.url))
