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

class UserViewSet(viewsets.ModelViewSet): 
    queryset = User.objects.all() 
    serializer_class = UserSerializer

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
def create_auth(request, user_hash):
    serialized = UserSerializer(data=request.DATA)
    if serialized.is_valid():
        user = User(
            serialized.init_data['email'],
            serialized.init_data['username'],
            serialized.init_data['password']
        )
        user.save()
    #if id is not null, search for profile and connect w user
    if user_hash != null:
        try:
            profile = Profile.objects.get(user_hash=user_hash)
        except profile.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        profile.user = user
        profile.save()

        return Response(serialized.data, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)


#create 2 views- one for manager, one for employee
@api_view(['POST'])
def onboard_manager(request, pk):
    data = OnboardManagerSerializer(request.body).data
    profile = Profile(
        user = request.user,
        name = data.name,
        email = data.email,
        location = data.location,
        isManager = True
        #need to add in auth0id here
    )
    profile.save()
    manager = Manager(profile = profile)
    manager.save()
    #added team creation here - how to return this as well?
    team = Team(manager= manager)
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

    serialized = PendingEmployeeSerializer(data=request.data, many=True)
    for employee in serialized:
        #getting hashed email object for user_hash
        hash_object = hashlib.sha256(data.email.encode('utf-8'))
        hex_dig = hash_object.hexdigest()

        pending_employee_profile = Profile(
            name = data.name,
            email = data.email,
            isManager = False,
            user_hash = hex_dig
        )
        Profile.save()
        pending_employee = Employee(profile = pending_employee_profile)
        pending_employee.save()

        team.pending_employees.add(pending_employee)
        team.save()
    #send each pending employee an email with a link which contains
    #their signup code
    #need to fill this out properly/check email integration
    # message = render_to_string('emails/activate_account.html', {
    #             'user': ,
    #             'domain': ,
    #             'uid': ,
    #             'token': ,
    #         })
    mail_subject = 'Activate your Good Neighbor Account!'
    to_email = data.email
    email = EmailMultiAlternatives(mail_subject, message, to=[to_email])
    email.content_subtype = 'html'
    mail.mixed_subtype = 'related'
    email.send()

#is this a post & patch?
#confusing
@api_view(['PATCH'])
def onboard_employee(request, pk):
    #adding employee to their team here by pk of team created
    #find employee obj based on pk somehow
    try:
        employee = Employee.objects.get(pk=pk)
    except employee.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    #get the team object from the employee based on pending list
    try:
        team = employee.team_set.first()
    except team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
        
    if request.method == 'PATCH':
       #am i allowed to do this
        employee.profile.user = request.user
        serializer = OnboardEmployeeSerializer(employee.profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            #return Response(serializer.data, status=status.HTTP_201_CREATED)
            # 
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    team.pending_employees.remove(employee)
    team.employees.add(employee)
    team.save()

    
    
    #used serializer I created for adding employee- how do i know 
    #if it will add the employee or replace the current ones?
    # serializer = TeamCreateSerializer(data = employee)
    # if serializer.is_valid():
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # return Response(EmployeeSerializer(employee).data)


#get for menu items on a specific team's menu
#returns serialized menu object which contains foodItems and their infos
#do i need to serialize this menu again lol
@api_view(['GET'])
def get_team_menu(request, pk):
    try:
        team = Team.objects.get(pk=pk)
    except team.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    serializer = MenuSerializer(data = team.get_menu)
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
