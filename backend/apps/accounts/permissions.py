
from rest_framework.permissions import BasePermission


class IsHRorAdminOrReadOnly(BasePermission):
    """
    Admin and HR can view and create employees.
    Managers can view employees but cannot create them.
    Employees cannot access the employee directory.
    """

    def has_permission(self, request, view):
        user = request.user

        if not user or not user.is_authenticated:
            return False

        if user.role in ["ADMIN", "HR"]:
            return True

        if user.role == "MANAGER" and request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        return False
