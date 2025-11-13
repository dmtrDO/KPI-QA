from django.test import TestCase
from django.urls import reverse, resolve
from main.views import index, login, teacher, discipline_requests, logout


class TestUrls(TestCase):
    def test_index_url_is_resolved(self):
        url = reverse("index")
        self.assertEqual(resolve(url).func, index)

    def test_login_url_is_resolved(self):
        url = reverse("login")
        self.assertEqual(resolve(url).func, login)

    def test_teacher_url_is_resolved(self):
        url = reverse("teacher")
        self.assertEqual(resolve(url).func, teacher)

    def test_logout_url_is_resolved(self):
        url = reverse("logout")
        self.assertEqual(resolve(url).func, logout)

    def test_discipline_requests_url_is_resolved(self):
        url = reverse("discipline_requests")
        self.assertEqual(resolve(url).func, discipline_requests)
