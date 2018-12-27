from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse


class FaviconTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        User.objects.create_user(username='tom', email='tom@dummy.com', password='asdf1234')

    def setUp(self):
        self.client.login(username='tom', password='asdf1234')
        User.objects.first()

    def test_home_url_status_code(self):
        url = reverse('favicon')
        response = self.client.get(url)
        self.assertEquals(response.status_code, 302)
