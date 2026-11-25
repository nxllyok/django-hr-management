from django.contrib import admin

from .models import Workplace


@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):
    list_display = ("name", "address")
    search_fields = ("name", "address")
