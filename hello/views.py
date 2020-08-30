from django.shortcuts import render, redirect
from django.http import HttpResponse
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponseRedirect
from django.core import serializers
from django.conf import settings
from django.contrib.auth import logout as log_out
from django.contrib.auth.decorators import login_required
import json
from rest_framework import authentication, generics, permissions, status
from urllib.parse import urlencode
from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

@api_view(['GET'])
@permission_classes([AllowAny])
def public(request):
    return JsonResponse({'message': 'Hello from a public endpoint! You don\'t need to be authenticated to see this.'})

@api_view(['GET'])
def private(request):
    return JsonResponse({'message': 'Hello from a private endpoint! You need to be authenticated to see this.'})

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

class FoodItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer

class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer

@api_view(['PATCH'])
def team_schedule(request, pk):
    """
    List all code snippets, or create a new snippet.
    """
    try:
        team = Team.objects.get(pk=pk)
    except Team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = TeamScheduleSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#create 2 views- one for manager, one for employee
def onboard_manager(request):
    data = OnboardManagerSerializer(request.body).data
    profile = Profile(
        name = data.name,
        email = data.email,
        location = data.location
    )
    profile.save()
    manager = Manager(profile = profile)
    manager.save()
    return Response(ManagerSerializer(manager).data)

def onboard_employee(request):
    data = OnboardEmployeeSerializer(request.body).data
    profile = Profile(
        name = data.name,
        email = data.email,
        location = data.location
    )
    profile.save()
    employee = Employee(profile = profile)
    employee.save()
    return Response(EmployeeSerializer(employee).data)


# @api_view(['GET'])
# def index(request):
#     user = request.user
#     if user.is_authenticated:
#         return Response("hello world")
#         #return redirect(dashboard)
#     else:
#         return Response("authentication error")
#         #return render(request, 'index.html')

# # @login_required
# def dashboard(request):
#     user = request.user
#     auth0user = user.social_auth.get(provider='auth0')
#     userdata = {
#         'user_id': auth0user.uid,
#         'name': user.first_name,
#         'picture': auth0user.extra_data['picture'],
#         'email': auth0user.extra_data['email'],
#     }

#     # return render(request, 'dashboard.html', {
#     #     'auth0User': auth0user,
#     #     'userdata': json.dumps(userdata, indent=4)
#     # })

# def logout(request):
#     log_out(request)
#     return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
#     logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
#                  (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
#     return HttpResponseRedirect(logout_url)



# def public(request):
#     return HttpResponse("You don't need to be authenticated to see this")


# @api_view(['GET'])
# def private(request):
#     return HttpResponse("You should not see this message if not authenticated!")
