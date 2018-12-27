from django.contrib.auth.models import User
from django.urls import reverse, resolve
from django.test import TestCase
from ..views import index, new_task
from ..models import Task
from ..forms import NewTaskForm


class IndexTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='tom', email='tom@dummy.com', password='asdf1234')
        User.objects.create_user(username='tomi', email='tomi@dummy.com', password='asdf1234')

    def setUp(self):
        self.client.login(username='tom', password='asdf1234')
        self.user = User.objects.first()
        Task.objects.create(name='another task', description='testing page', issued_by=self.user)

    def test_index_view_url_exists_at_desired_location(self):
        response = self.client.get('/todolist/')
        self.assertEqual(response.status_code, 200)

    def test_index_view_status_code(self):
        url = reverse('tdl:index')
        response = self.client.get(url, follow=True)
        self.assertEquals(response.status_code, 200)

    def test_index_view_uses_correct_template(self):
        response = self.client.get(reverse('tdl:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'tdl/index.html')

    def test_index_view_uses_base_template(self):
        response = self.client.get(reverse('tdl:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'base.html')

    def test_index_url_resolves_index_view(self):
        view = resolve(reverse('tdl:index'))
        self.assertEquals(view.func, index)

    def test_index_view_contains_link_new_task(self):
        new_task_url = reverse('tdl:new_task')
        index_url = reverse('tdl:index')
        response = self.client.get(index_url, follow=True)
        self.assertContains(response, 'href="{0}"'.format(new_task_url))

    def test_index_view_contains_edit_task_for_self_asserted_task_button(self):
        task_edit = reverse('tdl:task_edit', kwargs={'task_id': 1})
        index_url = reverse('tdl:index')
        response = self.client.get(index_url, follow=True)
        self.assertContains(response, 'href="{0}"'.format(task_edit))

    def test_index_view_does_not_contain_edit_task_button_for_others_users_asserted_task(self):
        self.client.logout()
        self.client.login(username='tomi', password='asdf1234')
        task_edit = reverse('tdl:task_edit', kwargs={'task_id': 1})
        index_url = reverse('tdl:index')
        response = self.client.get(index_url, follow=True)
        self.assertNotContains(response, 'href="{0}"'.format(task_edit))

    def test_index_view_contains_delete_task_for_self_asserted_task_button(self):
        task_delete = reverse('tdl:task_delete', kwargs={'task_id': 1})
        index_url = reverse('tdl:index')
        response = self.client.get(index_url, follow=True)
        self.assertContains(response, 'href="{0}"'.format(task_delete))

    def test_index_view_does_not_contain_delete_task_button_for_others_users_asserted_task(self):
        self.client.logout()
        self.client.login(username='tomi', password='asdf1234')
        task_delete = reverse('tdl:task_delete', kwargs={'task_id': 1})
        index_url = reverse('tdl:index')
        response = self.client.get(index_url, follow=True)
        self.assertNotContains(response, 'href="{0}"'.format(task_delete))

    def test_index_view_contains_done_task_for_self_asserted_task_button(self):
        task_done = reverse('tdl:task_done', kwargs={'task_id': 1})
        index_url = reverse('tdl:index')
        response = self.client.get(index_url, follow=True)
        self.assertContains(response, 'href="{0}"'.format(task_done))

    def test_index_view_contains_done_task_button_for_others_users_asserted_task(self):
        self.client.logout()
        self.client.login(username='tomi', password='asdf1234')
        task_done = reverse('tdl:task_done', kwargs={'task_id': 1})
        index_url = reverse('tdl:index')
        response = self.client.get(index_url, follow=True)
        self.assertContains(response, 'href="{0}"'.format(task_done))

    def test_index_view_contains_undone_task_for_self_asserted_task_button(self):
        task = Task.objects.get(pk=1)
        task.done = True
        task.save()
        task_undone = reverse('tdl:task_undone', kwargs={'task_id': 1})
        index_url = reverse('tdl:index')
        response = self.client.get(index_url, follow=True)
        self.assertContains(response, 'href="{0}"'.format(task_undone))

    def test_index_view_does_not_contain_undone_task_button_for_others_users_asserted_task(self):
        self.client.logout()
        self.client.login(username='tomi', password='asdf1234')
        task = Task.objects.get(pk=1)
        task.done = True
        task.save()
        task_undone = reverse('tdl:task_undone', kwargs={'task_id': 1})
        index_url = reverse('tdl:index')
        response = self.client.get(index_url, follow=True)
        self.assertNotContains(response, 'href="{0}"'.format(task_undone))

    def test_index_contains_link_for_password_change(self):
        password_url = reverse('accounts:password_change')
        index_url = reverse('tdl:index')
        response = self.client.get(index_url, follow=True)
        self.assertContains(response, 'href="{0}"'.format(password_url))

    def test_index_contains_link_for_logout(self):
        logout_url = reverse('accounts:logout')
        index_url = reverse('tdl:index')
        response = self.client.get(index_url, follow=True)
        self.assertContains(response, 'href="{0}"'.format(logout_url))

    def test_index_lists_all_tasks(self):
        response = self.client.get(reverse('tdl:index'))
        self.assertEqual(response.status_code, 200)
        self.assertNumQueries(1)
        Task.objects.create(name='second task',
                            description='second task description', issued_by=self.user)
        response_tasks = response.context['tasks'].values('name')
        dct = [dict(elem) for elem in response_tasks]
        names = [d['name'] for d in dct]
        self.assertTrue('another task' in names)
        self.assertTrue('second task' in names)
        self.assertNumQueries(2)


class LoginRequiredIndexTests(TestCase):
    def setUp(self):
        User.objects.create_user(username='tommy', email='tom@dumy.com', password='asdf1234')
        self.client.login(username='tommy', password='asdf1234')
        user = User.objects.first()
        self.client.logout()
        self.login_url = reverse('accounts:login')

    def test_login_redirection_index(self):
        url = reverse('tdl:index')
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, '{login_url}?next={url}'.format(
            login_url=self.login_url, url=url))
