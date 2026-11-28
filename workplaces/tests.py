from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.test import TestCase

from .models import Workplace

Employee = get_user_model()


class WorkplaceValidationTests(TestCase):
    def setUp(self):
        self.developer = Employee.objects.create_user(
            username="test_backend",
            password="test_password_123",
            first_name="Тест",
            last_name="Разработчик",
            position="BACKEND",
        )

        self.tester = Employee.objects.create_user(
            username="test_tester",
            password="test_password_123",
            first_name="Тест",
            last_name="Тестировщик",
            position="TESTER",
        )

        self.frontend = Employee.objects.create_user(
            username="test_frontend",
            password="test_password_123",
            first_name="Тест",
            last_name="Frontend",
            position="FRONTEND",
        )

    def test_tester_cannot_sit_next_to_backend(self):
        Workplace.objects.create(
            desk_number=100,
            employee=self.developer,
        )

        with self.assertRaises(ValidationError):
            Workplace.objects.create(
                desk_number=101,
                employee=self.tester,
            )

    def test_backend_can_sit_next_to_frontend(self):
        Workplace.objects.create(
            desk_number=200,
            employee=self.developer,
        )

        workplace = Workplace(
            desk_number=201,
            employee=self.frontend,
        )

        workplace.full_clean()

    def test_tester_can_sit_next_to_empty_desk(self):
        workplace = Workplace(
            desk_number=301,
            employee=self.tester,
        )

        workplace.full_clean()
