from django.contrib import admin

from .models import Workplace


@admin.register(Workplace)
class WorkplaceAdmin(admin.ModelAdmin):
    list_display = (
        "desk_number",
        "employee",
        "description",
    )
    search_fields = (
        "employee__username",
        "employee__first_name",
        "employee__last_name",
    )
