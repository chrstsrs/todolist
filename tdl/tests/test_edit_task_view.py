from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.test import TestCase

from ..models import Task
from ..views import task_edit
from ..forms import NewTaskForm


class EditTaskAuthenticatedUserTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='tommy', email='tommy@dumy.com', password='asdf1234')
        User.objects.create_user(username='tom', email='tom@dumy.com', password='asdf4321')

    def setUp(self):
        self.client.login(username='tommy', password='asdf1234')
        user = User.objects.first()
        Task.objects.create(name='another task', description='testing page', issued_by=user)

    def test_edit_view_url_exists_at_desired_location(self):
        response = self.client.get('/todolist/task_edit/1/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_edit_task_view_status_code_for_valid_task(self):
        url = reverse('tdl:task_edit', kwargs={'task_id': 1})
        response = self.client.get(url, follow=True)
        self.assertEquals(response.status_code, 200)

    def test_edit_view_uses_edit_template(self):
        response = self.client.get(reverse('tdl:task_edit', kwargs={'task_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tdl/edit.html')

    def test_edit_view_uses_base_template(self):
        response = self.client.get(reverse('tdl:task_edit', kwargs={'task_id': 1}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_edit_task_url_resolves_view(self):
        view = resolve(reverse('tdl:task_edit', kwargs={'task_id': 1}))
        self.assertEquals(view.func.view_class, task_edit)

    def test_edit_task_contains_form(self):
        url = reverse('tdl:task_edit', kwargs={'task_id': 1})
        response = self.client.get(url, follow=True)
        form = response.context.get('form')
        self.assertIsInstance(form, NewTaskForm)

    def test_csrf(self):
        url = reverse('tdl:task_edit', kwargs={'task_id': 1})
        response = self.client.get(url, follow=True)
        self.assertContains(response, 'csrfmiddlewaretoken')

    def test_edit_task_view_status_code_for_invalid_task(self):
        url = reverse('tdl:task_edit', kwargs={'task_id': 99})
        response = self.client.get(url, follow=True)
        self.assertEquals(response.status_code, 404)

    def test_edit_task_contains_link_for_index(self):
        url_index = reverse('tdl:index')
        url = reverse('tdl:task_edit', kwargs={'task_id': 1})
        response = self.client.get(url, follow=True)
        self.assertContains(response, 'href="{0}"'.format(url_index))

    def test_edit_task_valid_task_data(self):
        url = reverse('tdl:task_edit', kwargs={'task_id': 1})
        data = {
            'name': 'task2',
            'description': 'Testing data',
        }
        self.client.post(url, data, follow=True)
        url_index = reverse('tdl:index')
        self.client.get(url_index, follow=True)
        query = Task.objects.values()[0]
        self.assertEquals(data['name'], query['name'])
        self.assertEquals(data['description'], query['description'])
        self.assertEquals(query['issued_by_id'], 1)

    def test_edit_task_invalid_data(self):
        url = reverse('tdl:task_edit', kwargs={'task_id': 1})
        response = self.client.post(url, {}, follow=True)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_edit_task_invalid_data_empty_fields(self):
        url = reverse('tdl:task_edit', kwargs={'task_id': 1})
        data = {
            'name': "",
            'description': ""
        }
        response = self.client.post(url, {}, follow=True)
        form = response.context.get('form')
        self.assertEquals(response.status_code, 200)
        self.assertTrue(form.errors)

    def test_edit_task_invalid_user(self):
        self.client.logout()
        self.client.login(username='tom', password='asdf4321')
        url = reverse('tdl:task_edit', kwargs={'task_id': 1})
        response = self.client.get(url)
        self.assertEquals(response.status_code, 404)

    def test_index_contains_link_for_password_change(self):
        password_url = reverse('accounts:password_change')
        url = reverse('tdl:task_edit', kwargs={'task_id': 1})
        response = self.client.get(url, follow=True)
        self.assertContains(response, 'href="{0}"'.format(password_url))

    def test_index_contains_link_for_logout(self):
        logout_url = reverse('accounts:logout')
        url = reverse('tdl:task_edit', kwargs={'task_id': 1})
        response = self.client.get(url, follow=True)
        self.assertContains(response, 'href="{0}"'.format(logout_url))


class LoginRequiredEditTaskTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='tommy', email='tom@dumy.com', password='asdf1234')
        self.client.login(username='tommy', password='asdf1234')
        user = User.objects.first()
        Task.objects.create(name='another task', description='testing page', issued_by=user)
        self.client.logout()
        self.login_url = reverse('accounts:login')

    def test_login_redirection_task_edit(self):
        url = reverse('tdl:task_edit', kwargs={'task_id': 1})
        response = self.client.get(url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(
            login_url=self.login_url, url=url))
