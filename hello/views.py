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
from django.contrib.auth.models import User 
import hashlib
import requests

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

#test endpt
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def manager_auth(request):
#     return JsonResponse({'message': 'Hello from a public endpoint! You don\'t need to be authenticated to see this.'})


class UserViewSet(viewsets.ModelViewSet): 
    queryset = User.objects.all() 
    serializer_class = UserSerializer

class EmployeeViewSet(viewsets.ModelViewSet):
    queryset = Employee.objects.all().order_by('id')
    serializer_class = EmployeeSerializer 

class ManagerViewSet(viewsets.ModelViewSet):
    queryset = Manager.objects.all().order_by('id')
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

class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all().order_by('id')
    serializer_class = ProfileSerializer 

class FoodItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = FoodItem.objects.all()
    serializer_class = FoodItemSerializer

class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


@api_view(['PATCH'])
def team_schedule(request, pk):
    
    try:
        team = Team.objects.get(pk=pk)
    except team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = TeamScheduleSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#signup endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
def manager_auth(request):
    if request.method == "POST":

        serialized = UserSerializer(data=request.data)
        print(serialized.is_valid())
        if serialized.is_valid():
            print(serialized.validated_data)
            user = User(
                email = serialized.validated_data['email'],
                username = serialized.validated_data['username']
            )
            user.set_password(serialized.validated_data['password'])
            user.save()
    return JsonResponse({'message':'Hello World'})
    
#employee signup endpoint
@api_view(['POST'])
@permission_classes([AllowAny])
def employee_auth(request, user_hash):
    #if id is not null, search for profile and connect w user
    if user_hash == "":
        return JsonResponse({'message':'Must have an invite link/code to join team!'})
    if user_hash != "":
        print(user_hash)
        try:
            profile = Profile.objects.get(user_hash=user_hash)
        except profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

    print(profile)
    if profile.user is not None:
        return JsonResponse({'message':'This profile already has a user!'})

    serialized = UserSerializer(data=request.data)
    print(serialized.is_valid())
    if serialized.is_valid():
        print(serialized.validated_data)
        user = User(
            email = serialized.validated_data['email'],
            username = serialized.validated_data['username']
        )
        user.set_password(serialized.validated_data['password'])
        user.save()

        profile.user = user
        profile.save()

        return Response(serialized.data, status=status.HTTP_201_CREATED)
    
    return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)



#create 2 views- one for manager, one for employee
@api_view(['POST'])
def onboard_manager(request):
    serialized = OnboardManagerSerializer(data=request.data)
    print(serialized.is_valid())
    print(request.data['name'])
    if serialized.is_valid():
        profile = Profile(
            user = request.user,
            name = request.data['name'],
            email = request.data['email'],
            location = request.data['location'],
            isManager = True
        )
        profile.save()
        manager = Manager(profile = profile)
        manager.save()
        #added team creation here - how to return this as well?
        team = Team()
        team.save()
        team.manager.add(manager)
        team.save()
        return Response(ManagerSerializer(manager).data) 


#need to add endpoint for emailing employees for registration
# once their emails are inputted into page?
#add them to pending_employees in the team 
#this only adds one employee
#post & patch?
@api_view(['POST'])
def add_pending_employee(request, pk):
    try:
        team = Team.objects.get(pk=pk)
    except team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    data = request.data
    if isinstance(data, list):  # <- is the main logic
        print("yay")
        serialized = PendingEmployeeInfoSerializer(data=request.data, many=True)
    else:
        serialized = PendingEmployeeInfoSerializer(data=request.data)

    #print(team)
    #serialized = PendingEmployeeInfoSerializer(data=request.data, many=True)
    print(serialized.is_valid())
    if serialized.is_valid():
        #print(serialized)
        serialized_list = serialized.data[:]
        print(serialized_list)
        for employee in serialized_list:
            print(employee)
            #getting hashed email object for user_hash
            #print(employee.get('name'))
            hash_object = hashlib.sha256(employee.get('email').encode('utf-8'))
            hex_dig = hash_object.hexdigest()
            print(hex_dig)
            pending_employee_profile = Profile(
                name = employee.get('name'),
                email = employee.get('email'),
                isManager = False,
                user_hash = hex_dig
            )
            pending_employee_profile.save()
            pending_employee = Employee(profile=pending_employee_profile)
            pending_employee.save()
            #print(pending_employee)

            team.pending_employees.add(pending_employee)
            team.save()
    return JsonResponse({'message':'Hello World'})
    #send each pending employee an email with a link which contains
    #their signup code
    #need to fill this out properly/check email integration
    # message = render_to_string('emails/activate_account.html', {
    #             'user': ,
    #             'domain': ,
    #             'uid': ,
    #             'token': ,
    #         })
    # mail_subject = 'Activate your Good Neighbor Account!'
    # to_email = data.email
    # email = EmailMultiAlternatives(mail_subject, message, to=[to_email])
    # email.content_subtype = 'html'
    # mail.mixed_subtype = 'related'
    # email.send()

@api_view(['PATCH'])
def onboard_employee(request):
    #adding employee to their team here by pk of team created
    #find employee obj based on pk somehow
    try:
        profile = Profile.objects.get(user = request.user)
    except profile.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    print(profile)
    #get the team object from the employee based on pending list
    try:
        employee = Employee.objects.get(profile=profile)
    except employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    print(employee)

    try:
        team = employee.pending_employees_list.first()
    except team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    print(team)
    if request.method == 'PATCH':
    
        serializer = OnboardEmployeeSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    team.pending_employees.remove(employee)
    team.employees.add(employee)
    team.save()
    return JsonResponse({'message':'Hello World'})


    
    #used serializer I created for adding employee- how do i know 
    #if it will add the employee or replace the current ones?
    # serializer = TeamCreateSerializer(data = employee)
    # if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # return Response(EmployeeSerializer(employee).data)
@api_view(['PATCH'])
def set_team_menu(request, pk):
    try:
        team = Team.objects.get(pk=pk)
    except team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        serializer = TeamMenuSerializer(team, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#get for menu items on a specific team's menu
#returns serialized menu object which contains foodItems and their infos
#do i need to serialize this menu again lol
@api_view(['GET'])
def get_team_menu(request, pk):
    try:
        team = Team.objects.get(pk=pk)
    except team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    menu = team.get_menu()
    # response = requests.get('http://localhost:8000/api/menu/' + str(menu.id))
    # print(response)
    # todos = response.json()
    # return todos
    # print(menu.location)
    # print(menu.get_foodItems())

    print(menu)
    team_menu = Menu.objects.get(pk = menu.pk)
    print(team_menu)
    serializer = MenuSerializer(data = team.get_menu().__dict__)
    #print(serializer)
    print(serializer.is_valid())
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Post to create a user's preference

#Patch to update a user's Preference 
#find preference by user id, and then update it??
@api_view(['GET','PATCH'])
def choose_meal_preference(request, pk):
    #should I match the pk of the user & date here, or the pk of just the
    #Preference obj since it has already been created?
    if request.method == 'GET':
        data = PreferenceGetSerializer(request.body).data
        try:
            preference = Preference.objects.filter(user=pk, date = data.date).first()

        except preference.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
    #TODO: fix - would this work?
    if request.method == 'PATCH':
        try:
            preference = Preference.objects.filter(pk=pk)

        except preference.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = PreferenceChooseSerializer(preference, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    


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
