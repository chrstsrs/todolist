from django.contrib.auth.models import User
from django.urls import resolve, reverse
from django.test import TestCase

from ..models import Task
from ..views import task_done


class DoneChangesStateTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='tommy', email='tom@dumy.com', password='asdf1234')

    def setUp(self):
        self.client.login(username='tommy', password='asdf1234')
        user = User.objects.first()
        Task.objects.create(name='another task', description='testing page', issued_by=user)

    def test_done_view_url_exists_at_desired_location(self):
        response = self.client.get('/todolist/task_done/1/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_task_done_view_status_code_for_valid_task_accessed_by_name(self):
        url = reverse('tdl:task_done', kwargs={'task_id': 1})
        response = self.client.get(url)
        self.assertRedirects(response, reverse('tdl:index'),
                             status_code=302, target_status_code=200)

    def test_task_done_view_status_code_for_invalid_task(self):
        url = reverse('tdl:task_done', kwargs={'task_id': 99})
        response = self.client.get(url, follow=True)
        self.assertEquals(response.status_code, 404)

    def test_task_done_url_resolves_view(self):
        view = resolve(reverse('tdl:task_done', kwargs={'task_id': 1}))
        self.assertEquals(view.func, task_done)

    def test_task_done_view_uses_correct_template(self):
        response = self.client.get(reverse('tdl:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tdl/index.html')

    def test_task_done_view_uses_base_template(self):
        url = reverse('tdl:task_done', kwargs={'task_id': 1})
        response = self.client.get(url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')


class LoginRequiredTaskDoneTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='tommy', email='tom@dumy.com', password='asdf1234')
        self.client.login(username='tommy', password='asdf1234')
        user = User.objects.first()
        Task.objects.create(name='another task', description='testing page', issued_by=user)
        self.client.logout()
        self.login_url = reverse('accounts:login')

    def test_login_redirection_task_done(self):
        url = reverse('tdl:task_done', kwargs={'task_id': 1})
        response = self.client.get(url)
        self.assertRedirects(response, '{login_url}?next={url}'.format(
            login_url=self.login_url, url=url))
