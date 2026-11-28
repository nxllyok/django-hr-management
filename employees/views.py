from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import DetailView, ListView, TemplateView

from .models import Employee


class HomeView(TemplateView):
    template_name = "employees/home.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["employees"] = (
            Employee.objects.filter(is_active=True)
            .prefetch_related("employee_skills__skill")
            .order_by("last_name", "first_name")[:6]
        )
        return context


class EmployeeListView(ListView):
    model = Employee
    template_name = "employees/employee_list.html"
    context_object_name = "employees"

    def get_queryset(self):
        return (
            Employee.objects.filter(is_active=True)
            .prefetch_related("employee_skills__skill")
            .order_by("last_name", "first_name")
        )


class EmployeeDetailView(LoginRequiredMixin, DetailView):
    model = Employee
    template_name = "employees/employee_detail.html"
    context_object_name = "employee"

    def get_queryset(self):
        return Employee.objects.filter(is_active=True).prefetch_related(
            "employee_skills__skill", "gallery"
        )
