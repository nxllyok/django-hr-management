from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)

    class Meta:
        verbose_name = "Навык"
        verbose_name_plural = "Навыки"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Employee(AbstractUser):
    class Gender(models.TextChoices):
        MALE = "M", "Мужской"
        FEMALE = "F", "Женский"
        OTHER = "O", "Другой"

    middle_name = models.CharField(
        max_length=150,
        blank=True,
        verbose_name="Отчество",
    )
    gender = models.CharField(
        max_length=1,
        choices=Gender.choices,
        blank=True,
        verbose_name="Пол",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )
    skills = models.ManyToManyField(
        Skill,
        through="EmployeeSkill",
        related_name="employees",
        verbose_name="Навыки",
    )

    class Meta:
        verbose_name = "Сотрудник"
        verbose_name_plural = "Сотрудники"
        ordering = ["last_name", "first_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}".strip() or self.username


class EmployeeSkill(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="employee_skills",
        verbose_name="Сотрудник",
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        related_name="employee_skills",
        verbose_name="Навык",
    )
    level = models.PositiveSmallIntegerField(
        validators=[
            MinValueValidator(1),
            MaxValueValidator(10),
        ],
        verbose_name="Уровень владения",
    )

    class Meta:
        verbose_name = "Навык сотрудника"
        verbose_name_plural = "Навыки сотрудников"
        constraints = [
            models.UniqueConstraint(
                fields=["employee", "skill"],
                name="unique_employee_skill",
            )
        ]
        ordering = ["employee", "skill"]

    def __str__(self):
        return f"{self.employee} — {self.skill}: {self.level}/10"
