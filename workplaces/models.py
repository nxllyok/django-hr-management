from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models


class Workplace(models.Model):
    desk_number = models.PositiveIntegerField(
        unique=True,
        verbose_name="Номер рабочего места",
    )
    employee = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workplace",
        verbose_name="Сотрудник",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Дополнительная информация",
    )

    class Meta:
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочие места"
        ordering = ["desk_number"]

    def clean(self):
        super().clean()

        if not self.employee_id or self.desk_number is None:
            return

        tester_position = "TESTER"
        developer_positions = {"BACKEND", "FRONTEND"}

        employee_position = self.employee.position

        if employee_position not in (developer_positions | {tester_position}):
            return

        neighboring_workplaces = (
            Workplace.objects.filter(
                desk_number__in=[
                    self.desk_number - 1,
                    self.desk_number + 1,
                ]
            )
            .exclude(pk=self.pk)
            .select_related("employee")
        )

        for workplace in neighboring_workplaces:
            if not workplace.employee_id:
                continue

            neighboring_position = workplace.employee.position

            tester_next_to_developer = (
                employee_position == tester_position
                and neighboring_position in developer_positions
            )

            developer_next_to_tester = (
                employee_position in developer_positions
                and neighboring_position == tester_position
            )

            if tester_next_to_developer or developer_next_to_tester:
                raise ValidationError(
                    {
                        "desk_number": (
                            "Тестировщик не может занимать соседнее "
                            "рабочее место с разработчиком."
                        )
                    }
                )

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Рабочее место №{self.desk_number}"
