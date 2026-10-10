
from rest_framework import status
from rest_framework.test import APITestCase
from apps.accounts.models import User

class EmployeeAPITests(APITestCase):
    def test_employee_list_returns_200(self):
        response = self.client.get("/api/v1/employees/")

        self.assertEqual(
            response.status_code,
            status.HTTP_200_OK,
        )

    def test_create_employee(self):
        user = User.objects.create_user(
            username="testemployee",
            password="TestPass123!",
        )

        payload = {
            "employee_id": "EMP_TEST_001",
            "phone_number": "9876543210",
            "department": "IT",
            "designation": "Software Engineer",
            "joining_date": "2026-10-10",
            "employment_status": "ACTIVE",
            "user": user.id,
        }

        response = self.client.post(
            "/api/v1/employees/",
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, 201)
        self.assertEqual(
            response.data["employee_id"],
            "EMP_TEST_001",
        )
