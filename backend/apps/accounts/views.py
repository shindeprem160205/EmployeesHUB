
from rest_framework import generics
from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
