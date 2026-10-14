
from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers
from django.contrib.auth.password_validation import validate_password

from .models import Employee


User = get_user_model()


class EmployeeSerializer(serializers.ModelSerializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True, trim_whitespace=False)
    email = serializers.EmailField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = Employee
        fields = [
            "id",
            "username",
            "password",
            "email",
            "user",
            "employee_id",
            "phone_number",
            "department",
            "designation",
            "joining_date",
            "employment_status",
        ]
        read_only_fields = ["id", "user"]

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError(
                "A user with this username already exists."
            )
        return value

    @transaction.atomic
    def create(self, validated_data):
        username = validated_data.pop("username")
        password = validated_data.pop("password")
        email = validated_data.pop("email", "")

        user = User.objects.create_user(
            username=username,
            password=password,
            email=email,
            role=User.Role.EMPLOYEE,
        )

        return Employee.objects.create(user=user, **validated_data)
    def validate_password(self, value):
        validate_password(value)
        return Employee.objects.create(user=user, **validated_data)

    def validate_password(self, value):
        validate_password(value)
        return value
