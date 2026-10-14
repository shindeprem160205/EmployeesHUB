
from rest_framework import status
from rest_framework.test import APITestCase
from apps.accounts.models import Employee, User


class EmployeeAPITests(APITestCase):
    def test_weak_password_is_rejected(self):
        response = self.client.post(
            "/api/v1/employees/",
            self.employee_payload(
                username="weakpassworduser",
                password="123",
                employee_id="EMP_TEST_004",
            ),
            format="json",
        )

        self.assertEqual(
            response.status_code,
            status.HTTP_400_BAD_REQUEST,
        )
        self.assertFalse(
            User.objects.filter(username="weakpassworduser").exists()
        )


    def setUp(self):
        self.hr_user = User.objects.create_user(
            username="hr_user",
            password="TestPass123!",
            role="HR",
        )
        self.client.force_authenticate(user=self.hr_user)

    def employee_payload(self, **overrides):
        payload = {
            "username": "newemployee",
            "password": "EmployeePass123!",
            "email": "employee@example.com",
            "employee_id": "EMP_TEST_001",
            "phone_number": "9876543210",
            "department": "IT",
            "designation": "Software Engineer",
            "joining_date": "2026-10-10",
            "employment_status": "ACTIVE",
        }
        payload.update(overrides)
        return payload

    def test_employee_list_returns_200(self):
        manager = User.objects.create_user(
            username="listmanager",
            password="TestPass123!",
            role="MANAGER",
        )
        self.client.force_authenticate(user=manager)

        response = self.client.get("/api/v1/employees/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_employee(self):
        response = self.client.post(
            "/api/v1/employees/",
            self.employee_payload(),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["employee_id"], "EMP_TEST_001")

        employee = Employee.objects.get(employee_id="EMP_TEST_001")
        self.assertEqual(employee.user.username, "newemployee")
        self.assertEqual(employee.user.role, User.Role.EMPLOYEE)
        self.assertTrue(employee.user.check_password("EmployeePass123!"))
        self.assertNotIn("password", response.data)

    def test_duplicate_username_is_rejected(self):
        User.objects.create_user(
            username="existinguser",
            password="TestPass123!",
        )

        response = self.client.post(
            "/api/v1/employees/",
            self.employee_payload(
                username="existinguser",
                employee_id="EMP_TEST_002",
            ),
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_client_cannot_choose_user_or_privileged_role(self):
        other_user = User.objects.create_user(
            username="otheruser",
            password="TestPass123!",
            role="HR",
        )

        payload = self.employee_payload(
            username="secureemployee",
            employee_id="EMP_TEST_003",
            user=other_user.id,
            role="ADMIN",
        )

        response = self.client.post(
            "/api/v1/employees/",
            payload,
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        employee = Employee.objects.get(employee_id="EMP_TEST_003")
        self.assertNotEqual(employee.user_id, other_user.id)
        self.assertEqual(employee.user.role, User.Role.EMPLOYEE)
        self.assertNotIn("password", response.data)

    def test_login_returns_jwt_tokens(self):
        response = self.client.post(
            "/api/v1/token/",
            {
                "username": "hr_user",
                "password": "TestPass123!",
            },
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_jwt_access_token_can_access_employee_list(self):
        token_response = self.client.post(
            "/api/v1/token/",
            {
                "username": "hr_user",
                "password": "TestPass123!",
            },
            format="json",
        )

        access_token = token_response.data["access"]
        self.client.force_authenticate(user=None)
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
        manager = User.objects.create_user(
            username="manager_user",
            password="TestPass123!",
            role="MANAGER",
        )
        self.client.force_authenticate(user=manager)

        response = self.client.post(
            "/api/v1/employees/",
            {},
            format="json",
        )

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
