from django.shortcuts import render
from django.http import HttpResponse
#from rest_framework.views import api_view
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from django.core import serializers
from django.conf import settings
import json


# views.py
from rest_framework import viewsets
from .models import *
from .serializers import EmployeeSerializer

from .serializers import ManagerSerializer

from .serializers import TeamSerializer

from .serializers import RestaurantSerializer

from .serializers import FoodItemSerializer

from .serializers import MenuSerializer

from .serializers import *

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('email')
    serializer_class = EmployeeSerializer 

class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all().order_by('email')
    serializer_class = ManagerSerializer 

class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all().order_by('manager')
    serializer_class = TeamSerializer 

class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all().order_by('name')
    serializer_class = RestaurantSerializer 

class FoodItemViewSet(viewsets.ModelViewSet):
    queryset = FoodItem.objects.all().order_by('foodName')
    serializer_class = FoodItemSerializer 

class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.all().order_by('date')
    serializer_class = MenuSerializer 