
from rest_framework import generics
from .models import Employee
from .serializers import EmployeeSerializer
from .permissions import IsHRorAdminOrReadOnly


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer


from rest_framework import generics
from rest_framework.permissions import IsAuthenticated

from .models import Employee
from .serializers import EmployeeSerializer


class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsAuthenticated]



class EmployeeListCreateView(generics.ListCreateAPIView):
    queryset = Employee.objects.all()
    serializer_class = EmployeeSerializer
    permission_classes = [IsHRorAdminOrReadOnly]
