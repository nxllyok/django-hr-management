from django.db import models


class Employee(models.Model):
    first_name = models.CharField(
        max_length=100,
        verbose_name="Имя",
    )
    last_name = models.CharField(
        max_length=100,
        verbose_name="Фамилия",
    )
    email = models.EmailField(
        unique=True,
        verbose_name="Электронная почта",
    )
    position = models.CharField(
        max_length=100,
        verbose_name="Должность",
    )
    workplace = models.ForeignKey(
        "workplaces.Workplace",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="employees",
        verbose_name="Рабочее место",
    )

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["last_name", "first_name"]
