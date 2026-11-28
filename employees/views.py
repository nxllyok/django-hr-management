from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.views.generic import DetailView, ListView, TemplateView

from .models import Employee


def get_experience_days(employee):
    """Calculate an employee's experience in days."""
    today = timezone.localdate()
    return max((today - employee.hire_date).days, 0)


def optimize_employee_queryset(queryset):
    """Reduce database queries for employee-related information."""
    return queryset.select_related(
        "workplace"
    ).prefetch_related(
        "employee_skills__skill",
        "gallery",
    )


class HomeView(TemplateView):
    template_name = "employees/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["employee_count"] = Employee.objects.count()

        employees = optimize_employee_queryset(
            Employee.objects.filter(is_active=True).order_by(
                "-hire_date",
                "-id",
            )
        )[:4]

        context["employees"] = list(employees)

        for employee in context["employees"]:
            employee.experience_days = get_experience_days(employee)

        return context


class EmployeeListView(ListView):
    model = Employee
    template_name = "employees/employee_list.html"
    context_object_name = "employees"
    paginate_by = 10

    def get_queryset(self):
        return optimize_employee_queryset(
            Employee.objects.filter(is_active=True).order_by(
                "last_name",
                "first_name",
            )
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        for employee in context["employees"]:
            employee.experience_days = get_experience_days(employee)

        return context


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = "employees/employee_detail.html"
    context_object_name = "employee"

    def get_queryset(self):
        return optimize_employee_queryset(
            Employee.objects.filter(is_active=True)
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        employee = self.object
        gallery = list(employee.gallery.all())

        context["experience_days"] = get_experience_days(employee)
        context["main_photo"] = gallery[0] if gallery else None
        context["extra_gallery"] = gallery[1:]

        return context
