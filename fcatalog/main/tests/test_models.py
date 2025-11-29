from datetime import datetime, timezone as dt_timezone
from unittest.mock import Mock, patch

from django.contrib.auth.models import User
from django.test import TestCase

from main.models import Discipline, Teacher

DEFAULT_TEACHER_EMAIL = "teacher@example.com"
DEFAULT_ADMIN_USERNAME = "admin"
DEFAULT_ADMIN_EMAIL = "admin@example.com"
DEFAULT_PASSWORD = "strong_pass"
DEFAULT_TITLE = "Linear Algebra"
DEFAULT_DESCRIPTION = "Test discipline description"
EXPECTED_TIMESTAMP = datetime(2023, 1, 1, 12, 0, tzinfo=dt_timezone.utc)


class TeacherModelTests(TestCase):
    def test_teacher_str_returns_email(self) -> None:
        teacher = Teacher.objects.create(
            email=DEFAULT_TEACHER_EMAIL, password=DEFAULT_PASSWORD
        )

        self.assertEqual(str(teacher), DEFAULT_TEACHER_EMAIL)
        self.assertGreater(len(teacher.email), 0)

    def test_teacher_str_with_double(self) -> None:
        teacher_double = Mock(spec=Teacher)
        teacher_double.email = DEFAULT_TEACHER_EMAIL

        self.assertEqual(Teacher.__str__(teacher_double), DEFAULT_TEACHER_EMAIL)
        self.assertIsInstance(teacher_double.email, str)


class DisciplineModelTests(TestCase):
    def setUp(self) -> None:
        self.teacher = Teacher.objects.create(
            email=DEFAULT_TEACHER_EMAIL, password=DEFAULT_PASSWORD
        )
        self.admin = User.objects.create_user(
            username=DEFAULT_ADMIN_USERNAME,
            email=DEFAULT_ADMIN_EMAIL,
            password=DEFAULT_PASSWORD,
        )

    def test_discipline_defaults(self) -> None:
        discipline = Discipline.objects.create(
            title=DEFAULT_TITLE,
            description=DEFAULT_DESCRIPTION,
            teacher=self.teacher,
            admin=self.admin,
        )

        self.assertEqual(str(discipline), DEFAULT_TITLE)
        self.assertFalse(discipline.is_approved)
        self.assertIsNotNone(discipline.created_date)
        self.assertEqual(discipline.teacher, self.teacher)
        self.assertEqual(discipline.admin, self.admin)

    @patch("django.utils.timezone.now", autospec=True)
    def test_discipline_created_date_uses_timezone_stub(self, mocked_now) -> None:
        mocked_now.return_value = EXPECTED_TIMESTAMP

        discipline = Discipline.objects.create(
            title=DEFAULT_TITLE,
            description=DEFAULT_DESCRIPTION,
            teacher=self.teacher,
            admin=self.admin,
        )

        self.assertEqual(discipline.created_date, EXPECTED_TIMESTAMP)
        mocked_now.assert_called_once()
