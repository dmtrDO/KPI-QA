from django.test import TestCase
from unittest.mock import patch
from django.urls import reverse
from main.forms import TeacherLoginForm, AddDisciplineForm



class TestTeacherLoginForm(TestCase):
    def testWithCorrectData(self):
        form = TeacherLoginForm(
            data={
                "email": "test@example.com",
                "password": "123456",
            }
        )
        self.assertTrue(form.is_valid())

    def testWithEmptyData(self):
        form = TeacherLoginForm(data={})
        self.assertTrue(form.is_valid())

    def testFieldsExist(self):
        form = TeacherLoginForm()
        self.assertIn("email", form.fields)
        self.assertIn("password", form.fields)


class TestCallTeacherLoginForm(TestCase):

    @patch("main.views.TeacherLoginForm")
    def testCallForm(self, mock_form_out):
        mock_form = mock_form_out.return_value

        mock_form.is_valid.return_value = True                  # stub
        mock_form.cleaned_data = {
            "email": "random@gmail.com",
            "password": "12345678",
        }

        response = self.client.post(reverse("login"))

        self.assertEqual(response.status_code, 200)

        mock_form.is_valid.assert_called_once()                 # mock


class TestAddDisciplineForm(TestCase):
    def testWithCorrectData(self):
        form = AddDisciplineForm(
            data={
                "title": "Математика",
                "description": "Опис дисципліни",
            }
        )
        self.assertTrue(form.is_valid())

    def testInvalidFormWithoutTitle(self):
        form = AddDisciplineForm(
            data={
                "description": "Опис дисципліни",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("title", form.errors)

    def testInvalidFormWithoutDescription(self):
        form = AddDisciplineForm(
            data={
                "title": "Математика",
            }
        )
        self.assertFalse(form.is_valid())
        self.assertIn("description", form.errors)

    def testFieldsExist(self):
        form = AddDisciplineForm()
        self.assertIn("title", form.fields)
        self.assertIn("description", form.fields)
