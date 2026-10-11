
from rest_framework import status
from rest_framework.test import APITestCase
from apps.accounts.models import Employee, User


class EmployeeAPITests(APITestCase):

    def test_employee_list_returns_200(self):
        user = User.objects.create_user(
            username="listuser",
            password="TestPass123!",
            role="MANAGER",
        )
        self.client.force_authenticate(user=user)

        response = self.client.get("/api/v1/employees/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_employee(self):
        user = User.objects.create_user(
            username="testemployee",
            password="TestPass123!",
            role="HR",
        )
        self.client.force_authenticate(user=user)

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

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["employee_id"], "EMP_TEST_001")

    def test_login_returns_jwt_tokens(self):
        User.objects.create_user(
            username="jwtuser",
            password="TestPass123!",
        )

        response = self.client.post(
            "/api/v1/token/",
            {
                "username": "jwtuser",
                "password": "TestPass123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_jwt_access_token_can_access_employee_list(self):
        User.objects.create_user(
            username="tokenuser",
            password="TestPass123!",
            role="MANAGER",
        )

        token_response = self.client.post(
            "/api/v1/token/",
            {
                "username": "tokenuser",
                "password": "TestPass123!",
            },
            format="json",
        )

        access_token = token_response.data["access"]
        self.client.credentials(
            HTTP_AUTHORIZATION=f"Bearer {access_token}"
        )

        response = self.client.get("/api/v1/employees/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_employee_cannot_access_employee_directory(self):
        user = User.objects.create_user(
            username="regular_employee",
            password="TestPass123!",
            role="EMPLOYEE",
        )
        self.client.force_authenticate(user=user)

        response = self.client.get("/api/v1/employees/")

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_manager_cannot_create_employee(self):
        user = User.objects.create_user(
            username="manager_user",
            password="TestPass123!",
            role="MANAGER",
        )
        self.client.force_authenticate(user=user)

        response = self.client.post(
            "/api/v1/employees/",
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_employee_uses_authenticated_user(self):
        hr_user = User.objects.create_user(
            username="hr_security_test",
            password="TestPass123!",
            role="HR",
        )
        other_user = User.objects.create_user(
            username="other_security_test",
            password="TestPass123!",
            role="EMPLOYEE",
        )
        self.client.force_authenticate(user=hr_user)

        payload = {
            "employee_id": "EMP_SECURITY_001",
            "phone_number": "9876543210",
            "department": "IT",
            "designation": "Software Engineer",
            "joining_date": "2026-10-11",
            "employment_status": "ACTIVE",
            "user": other_user.id,
        }

        response = self.client.post(
            "/api/v1/employees/",
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        employee = Employee.objects.get(employee_id="EMP_SECURITY_001")
        self.assertEqual(employee.user_id, hr_user.id)
        self.assertNotEqual(employee.user_id, other_user.id)
