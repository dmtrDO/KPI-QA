from django.test import TestCase
from django.urls import reverse, resolve
from main.views import index, login, teacher, discipline_requests, logout


class TestUrls(TestCase):
    def test_index_url_is_resolved(self):
        url = reverse("index")
        self.assertEqual(resolve(url).func, index)
