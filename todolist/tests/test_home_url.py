from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from tdl.views import index


class HomeUrlTests(TestCase):
    def test_home_url_exists_at_desired_location(self):
        response = self.client.get('/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_home_url_status_code(self):
        url = reverse('home')
        response = self.client.get(url, follow=True)
        self.assertEquals(response.status_code, 200)

    def test_home_url_redirects(self):
        User.objects.create_user(username='tom', email='tom@dummy.com', password='asdf1234')
        self.client.login(username='tom', password='asdf1234')
        self.user = User.objects.first()
        url = reverse('home')
        url_index = reverse('tdl:index')
        response = self.client.get(url, follow=True)
        self.assertRedirects(response, url_index)
