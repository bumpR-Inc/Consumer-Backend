from django.shortcuts import render
from django.http import HttpResponse

# views.py
from rest_framework import viewsets

from .serializers import EmployeeSerializer
from .models import Employee


class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('email')
    serializer_class = EmployeeSerializer