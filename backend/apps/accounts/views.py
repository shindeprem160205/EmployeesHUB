
from rest_framework import generics

from .models import Employee
from .serializers import EmployeeSerializer
from .permissions import IsHRorAdminOrReadOnly


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsHRorAdminOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
