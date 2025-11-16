from django.test import TestCase
from main.models import Discipline, Teacher
from main.views import download, teacher
from django.http import FileResponse
from django.urls import reverse
from unittest.mock import patch, MagicMock


class TestViews(TestCase):
    def test_download(self):
        disciplines = Discipline.objects.all()
        self.assertIsInstance(download(disciplines), FileResponse)

    @patch("main.views.Discipline.objects.all")
    def test_download_with_mock(self, mock_all):
        mock_all.return_value = [MagicMock(), MagicMock()]
        self.assertIsInstance(download(mock_all), FileResponse)

    def test_logged_teacher(self):
        self.teacher = Teacher.objects.create(email="teach@gmail.com", password="12345")
        session = self.client.session
        session["email"] = self.teacher.email
        session.save()
        response = self.client.get(reverse("teacher"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "teacher.html")

    # @patch("main.views.Teacher.objects.first")
    # def test_logged_teacher_with_mock(self):
    #     self.teacher = Teacher.objects.first()
    #     session = self.client.session
    #     session["email"] = self.teacher.email
    #     session.save()
    #     response = self.client.get(reverse("teacher"))
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTemplateUsed(response, "teacher.html")

    def test_unlogged_teacher(self):
        response = self.client.get(reverse("teacher"))
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("login"))
