from django.db import models


class Workplace(models.Model):
    name = models.CharField(
        max_length=150,
        verbose_name="Название рабочего места",
    )
    address = models.CharField(
        max_length=255,
        verbose_name="Адрес",
    )
    description = models.TextField(
        blank=True,
        verbose_name="Описание",
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Рабочее место"
        verbose_name_plural = "Рабочие места"
        ordering = ["name"]
