from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Employee, EmployeeSkill, Skill


@admin.register(Employee)
class EmployeeAdmin(UserAdmin):
    list_display = (
        "username",
        "first_name",
        "last_name",
        "email",
        "gender",
        "is_staff",
    )
    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
    )
    list_filter = (
        "gender",
        "is_staff",
        "is_active",
    )
    fieldsets = UserAdmin.fieldsets + (
        (
            "Дополнительная информация",
            {
                "fields": (
                    "middle_name",
                    "gender",
                    "description",
                )
            },
        ),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ("name", "description")
    search_fields = ("name",)


@admin.register(EmployeeSkill)
class EmployeeSkillAdmin(admin.ModelAdmin):
    list_display = ("employee", "skill", "level")
    list_filter = ("skill", "level")
    search_fields = (
        "employee__username",
        "employee__first_name",
        "employee__last_name",
        "skill__name",
    )
