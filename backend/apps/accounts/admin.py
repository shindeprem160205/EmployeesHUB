
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("EmployeeHub Details", {"fields": ("role",)}),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        ("EmployeeHub Details", {"fields": ("role",)}),
    )

    list_display = (
        "username",
        "email",
        "first_name",
        "last_name",
        "role",
        "is_staff",
    )
    list_filter = ("role", "is_staff", "is_active")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "employee_id",
        "user",
        "department",
        "designation",
        "joining_date",
        "employment_status",
    )
    list_filter = ("department", "employment_status")
    search_fields = (
        "employee_id",
        "user__username",
        "user__email",
        "department",
    )
    ordering = ("employee_id",)
