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
from functools import wraps
import jwt
from datetime import datetime
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from email.mime.image import MIMEImage

from rest_framework import viewsets
from .models import *
from .serializers import *
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

def get_token_auth_header(request):
    """Obtains the Access Token from the Authorization Header
    """
    auth = request.META.get("HTTP_AUTHORIZATION", None)
    parts = auth.split()
    token = parts[1]

    return token

def requires_scope(required_scope):
    """Determines if the required scope is present in the Access Token
    Args:
        required_scope (str): The scope required to access the resource
    """
    def require_scope(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            token = get_token_auth_header(args[0])
            decoded = jwt.decode(token, verify=False)
            if decoded.get("scope"):
                token_scopes = decoded["scope"].split()
                for token_scope in token_scopes:
                    if token_scope == required_scope:
                        return f(*args, **kwargs)
            response = JsonResponse({'message': 'You don\'t have access to this resource'})
            response.status_code = 403
            return response
        return decorated
    return require_scope

@api_view(['GET'])
@permission_classes([AllowAny])
def public(request):
    return JsonResponse({'message': 'Hello from a public endpoint! You don\'t need to be authenticated to see this.'})

@api_view(['GET'])
def private(request):
    return JsonResponse({'message': 'Hello from a private endpoint! You need to be authenticated to see this.'})

@api_view(['GET'])
@requires_scope('read:connections')
def private_scoped(request):
    return JsonResponse({'message': 'Hello from a private endpoint! You need to be authenticated and have a scope of read:messages to see this.'})

# def email_preview(request):
#     return render(request, 'email.html', {'employee': 'Bob', 'manager': 'Samantha'})

#test endpt
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def manager_auth(request):
#     return JsonResponse({'message': 'Hello from a public endpoint! You don\'t need to be authenticated to see this.'})

@permission_classes([AllowAny])
class UserViewSet(viewsets.ModelViewSet): 
    queryset = User.objects.all() 
    serializer_class = UserSerializer

@permission_classes([AllowAny])
class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

@permission_classes([AllowAny])
class ProfileDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer

@permission_classes([AllowAny])
class RestaurantViewSet(viewsets.ModelViewSet):
    queryset = Restaurant.objects.all().order_by('name')
    serializer_class = RestaurantSerializer

@permission_classes([AllowAny])
class RestaurantDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Restaurant.objects.all().order_by('name')
    serializer_class = RestaurantSerializer

@permission_classes([AllowAny])
class RestaurantCreate(generics.CreateAPIView):
    queryset = Restaurant.objects.all().order_by('name')
    serializer_class = RestaurantSerializer

@permission_classes([AllowAny])
class MenuItemSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all().order_by('restaurant')
    serializer_class = MenuItemSerializer

@permission_classes([AllowAny])
class MenuItemDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = MenuItem.objects.all().order_by('restaurant')
    serializer_class = MenuItemSerializer

@permission_classes([AllowAny])
class MenuItemCreate(generics.CreateAPIView):
    queryset = MenuItem.objects.all().order_by('restaurant')
    serializer_class = MenuItemSerializer

@permission_classes([AllowAny])
class ScheduleViewSet(viewsets.ModelViewSet):
    queryset = Schedule.objects.all().order_by('date')
    serializer_class = ScheduleSerializer

@permission_classes([AllowAny]) 
class ScheduleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Schedule.objects.all().order_by('date')
    serializer_class = ScheduleSerializer

@permission_classes([AllowAny])
class ScheduleCreate(generics.CreateAPIView):
    queryset = Schedule.objects.all().order_by('restaurant')
    serializer_class = ScheduleSerializer

@permission_classes([AllowAny])
class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().order_by('restaurant')
    serializer_class = OrderSerializer

@permission_classes([AllowAny])
class OrderDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all().order_by('restaurant')
    serializer_class = OrderSerializer

# @permission_classes([AllowAny])
# class OrderCreate(generics.CreateAPIView):
#     queryset = Order.objects.all().order_by('restaurant')
#     serializer_class = OrderSerializer

#@permission_classes([AllowAny])
#get current day schedule, if doesnt exist, create a new
#add to popularity of menuItem
@api_view(['POST'])
def OrderCreate(request):
    print("finddd")
    print(request.user)

    serialized = OrderCreateSerializer(data=request.data)
    print(serialized.is_valid())
    user = Profile.objects.get(user = request.user)
    if user is None:
        return("You must be logged in to order!")
    
    date = request.data['deliveryTime']
    date_time_obj = datetime.strptime(date, '%Y-%m-%d')

    if not Schedule.objects.filter(date = date_time_obj).exists():
        schedule = Schedule(
            restaurant = Restaurant.objects.get(pk=request.data['restaurant']),
            date = date_time_obj,
            specific_quota_status = False,
            quota = 0,
            numOrders =1
        )
        schedule.save()
    else:
        schedule = Schedule.objects.get(date = date_time_obj)
        schedule.numOrders += 1

    
    if serialized.is_valid():
        order = Order(
            user = Profile.objects.get(user = request.user),
            restaurant = Restaurant.objects.get(pk=request.data['restaurant']),
            schedule = schedule,
            orderTime = datetime.now(),
            deliveryMade = False,
            deliveryTime = request.data['deliveryTime'],
            location = request.data['location'],
            pricePaid = request.data['pricePaid']
         )
        order.save()

    menuItems = request.data['menuItems']
    for m in menuItems:
        menuItem = MenuItem.objects.get(pk = m)
        if menuItem is not None:

            orderItem = OrderItem(
                order = order,
                menuItem = menuItem
            )
            orderItem.save()

            menuItem.popularity += 1
    return Response(serialized.data, status=status.HTTP_201_CREATED)
    

#returns orders of specific user
@permission_classes([AllowAny])
@api_view(['GET'])
def user_orders(request, user):
    
    orders = Order.objects.filter(user = request.user)
    if orders is None:
        return None

    serializer = OrderSerializer(orders, many= True)

    # if serializer.is_valid():
    #     print(serializer)
    #     serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    # else:
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#return orders of user past current time
@permission_classes([AllowAny])
@api_view(['GET'])
def user_current_orders(request, user):

    orders = Order.objects.filter(user = request.user)
    if orders is None:
        return None

    orders = [x for x in orders if (x.deliveryTime.timestamp() > datetime.now().timestamp() and x.deliveryMade is False)]
    if orders is None:
        print(orders)
        return None

    serializer = OrderSerializer(orders, many= True)

    # if serializer.is_valid():
    #     print(serializer)
    #     serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    # else:
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#return orders of specific restaurant

@api_view(['GET'])
@permission_classes([AllowAny])
def restaurant_orders(request, restaurant):
    orders = Order.objects.filter(restaurant = restaurant)
    if orders is None:
        return None

    serializer = OrderSerializer(orders, many= True)
    print(orders)

    #if serializer.is_valid():
        #print(serializer)
        #serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    # else:
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



#return orders of specific restaurant after now
@api_view(['GET'])
@permission_classes([AllowAny])
def restaurant_current_orders(request, restaurant):


    orders = Order.objects.filter(restaurant =restaurant)
    if orders is None:
        print(orders)
        return None


    orders = [x for x in orders if (x.deliveryTime.timestamp() > datetime.now().timestamp() and x.deliveryMade is False)]
    if orders is None:
        print(orders)
        return None

    serializer = OrderSerializer(orders, many= True)

    # if serializer.is_valid():
    #     print(serializer)
    #     serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    # else:
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#return restaurant orders on a specific date
@api_view(['GET'])
@permission_classes([AllowAny])
def restaurant_day_orders(request, restaurant, date):

    orders = Order.objects.filter(restaurant = restaurant)
    if orders is None:
        return None

    date_time_obj = datetime.strptime(date, '%Y-%m-%d')
    #%H:%M:%S.%f')
    orders = [x for x in orders if x.deliveryTime.date() == date_time_obj.date()]
    if orders is None:
        return None

    serializer = OrderSerializer(orders, many= True)

    # if serializer.is_valid():
    #     print(serializer)
    #     serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)
    # else:
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)





# def index(request):
#     user = request.user
#     if user.is_authenticated:
#         return redirect(dashboard)
#     else:
#         return render(request, 'index.html')

# @login_required
# def dashboard(request):
#     user = request.user
#     auth0user = user.social_auth.get(provider='auth0')
#     userdata = {
#         'user_id': auth0user.uid,
#         'name': user.first_name,
#         'picture': auth0user.extra_data['picture'],
#         'email': auth0user.extra_data['email'],
#     }

#     return render(request, 'dashboard.html', {
#         'auth0User': auth0user,
#         'userdata': json.dumps(userdata, indent=4)
#     })

# def logout(request):
#     log_out(request)
#     return_to = urlencode({'returnTo': request.build_absolute_uri('/')})
#     logout_url = 'https://%s/v2/logout?client_id=%s&%s' % \
#                  (settings.SOCIAL_AUTH_AUTH0_DOMAIN, settings.SOCIAL_AUTH_AUTH0_KEY, return_to)
#     return HttpResponseRedirect(logout_url)


# class EmployeeViewSet(viewsets.ModelViewSet):
#     queryset = Employee.objects.all().order_by('id')
#     serializer_class = EmployeeSerializer 

# class ManagerViewSet(viewsets.ModelViewSet):
#     queryset = Manager.objects.all().order_by('id')
#     serializer_class = ManagerSerializer 

# class TeamViewSet(viewsets.ModelViewSet):
#     queryset = Team.objects.all().order_by('manager')
#     serializer_class = TeamSerializer 

# class RestaurantViewSet(viewsets.ModelViewSet):
#     queryset = Restaurant.objects.all().order_by('name')
#     serializer_class = RestaurantSerializer 

# class FoodItemViewSet(viewsets.ModelViewSet):
#     queryset = FoodItem.objects.all().order_by('foodName')
#     serializer_class = FoodItemSerializer 

# class MenuViewSet(viewsets.ModelViewSet):
#     queryset = Menu.objects.all().order_by('date')
#     serializer_class = MenuSerializer 

# class ProfileViewSet(viewsets.ModelViewSet):
#     queryset = Profile.objects.all().order_by('id')
#     serializer_class = ProfileSerializer 

# class FoodItemDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = FoodItem.objects.all()
#     serializer_class = FoodItemSerializer

# class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Team.objects.all()
#     serializer_class = TeamSerializer

# class PreferenceViewSet(viewsets.ModelViewSet):
#     queryset = Preference.objects.all().order_by('date')
#     serializer_class = PreferenceSerializer 


# @api_view(['PATCH'])
# def team_schedule(request, pk):
    
#     try:
#         team = Team.objects.get(pk=pk)
#     except team.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'PATCH':
#         serializer = TeamScheduleSerializer(team, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# #signup endpoint
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def manager_auth(request):
#     if request.method == "POST":

#         serialized = UserSerializer(data=request.data)
#         print(serialized.is_valid())
#         if serialized.is_valid():
#             print(serialized.validated_data)
#             # user = User(
#             #     email = serialized.validated_data['email'],
#             #     username = serialized.validated_data['username']
#             # )
#             # user.set_password(serialized.validated_data['password'])
#             user = User.objects.create_user(serialized.validated_data['username'], serialized.validated_data['email'], serialized.validated_data['password'])
#             user.save()
#             try:
#                 print(user)
#             except user.DoesNotExist:
#                 return JsonResponse({'message':'Unable to create user'})
            
#             return JsonResponse({'message':'Hello World'})
#     return JsonResponse({'message':'Unable to create user'})
# #employee signup endpoint
# @api_view(['POST'])
# @permission_classes([AllowAny])
# def employee_auth(request, user_hash):
#     #if id is not None, search for profile and connect w user
#     if user_hash == "":
#         return JsonResponse({'message':'Must have an invite link/code to join team!'})
#     if user_hash != "":
#         print(user_hash)
#         try:
#             profile = Profile.objects.get(user_hash=user_hash)
#         except profile.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#     print(profile)
#     if profile.user is not None:
#         return JsonResponse({'message':'This profile already has a user!'})

#     serialized = UserSerializer(data=request.data)
#     print(serialized.is_valid())
#     if serialized.is_valid():
#         print(serialized.validated_data)
#         # user = User(
#         #     email = serialized.validated_data['email'],
#         #     username = serialized.validated_data['username']
#         # )
#         # user.set_password(serialized.validated_data['password'])
#         # user.save()
#         user = User.objects.create_user(serialized.validated_data['username'], serialized.validated_data['email'], serialized.validated_data['password'])
#         user.save()

#         profile.user = user
#         profile.save()
#         try:
#             print(user)
#         except user.DoesNotExist:
#             return JsonResponse({'message':'Unable to create user'})

#         return Response(serialized.data, status=status.HTTP_201_CREATED)
    
#     return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)



# #create 2 views- one for manager, one for employee
# @api_view(['POST'])
# def onboard_manager(request):
#     serialized = OnboardManagerSerializer(data=request.data)
#     print(serialized.is_valid())
#     print(request.data['name'])
#     if serialized.is_valid():
#         profile = Profile(
#             user = request.user,
#             name = request.data['name'],
#             email = request.data['email'],
#             location = request.data['location'],
#             isManager = True
#         )
#         profile.save()
#         manager = Manager(profile = profile)
#         manager.save()
#         #added team creation here - how to return this as well?
#         team = Team()
#         team.save()
#         team.manager.add(manager)
#         team.save()
#         return Response(ManagerSerializer(manager).data) 

# @api_view(['GET'])
# def email_test(request):
#     try:
#         profile = Profile.objects.get(user = request.user)
#     except profile.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)


#     # message = render_to_string('emails/activate_account.html', {
#     #             'user': request.user,
#     #             'domain': current_site.domain,
#     #             'uid': urlsafe_base64_encode(force_bytes(user.pk)),
#     #             'token': account_activation_token.make_token(user),
#     #         })
#     link = "https://goodneighbordelivery.herokuapp.com/?route=2&code=" + profile.user_hash 
#     print(profile.user_hash, link)
#     fp = open('static/img/logo.png', 'rb')
#     logo = MIMEImage(fp.read())
#     logo.add_header('Content-ID', '<logo>')
#     message = render_to_string('email.html', {
#         'img1': logo, 
#         'employee': profile.name,
#         'manager': profile.name,
#         'link': link,
#     })
#     mail_subject = 'Activate your Good Neighbor Account!'
#     to_email = profile.email
#     email = EmailMultiAlternatives(mail_subject, message, to=[to_email])
#     email.content_subtype = 'html'
#     email.mixed_subtype = 'related'
#     # email.attach(logo)
#     email.send()
#     return JsonResponse({'message':'Hello World'})

# #need to add endpoint for emailing employees for registration
# # once their emails are inputted into page?
# #add them to pending_employees in the team 
# #this only adds one employee
# #post & patch?
# @api_view(['POST'])
# def add_pending_employee(request, pk):
#     try:
#         team = Team.objects.get(pk=pk)
#     except team.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     try:
#         profile_manager = Profile.objects.get(user = request.user)
#     except profile_manager.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     data = request.data
#     if isinstance(data, list):  # <- is the main logic
#         print("yay")
#         serialized = PendingEmployeeInfoSerializer(data=request.data, many=True)
#     else:
#         serialized = PendingEmployeeInfoSerializer(data=request.data)

#     #print(team)
#     #serialized = PendingEmployeeInfoSerializer(data=request.data, many=True)
#     print(serialized.is_valid())
#     if serialized.is_valid():
#         #print(serialized)
#         serialized_list = serialized.data[:]
#         print(serialized_list)
#         for employee in serialized_list:
#             print(employee)
#             #getting hashed email object for user_hash
#             #print(employee.get('name'))
#             hash_object = hashlib.sha256(employee.get('email').encode('utf-8'))
#             hex_dig = hash_object.hexdigest()
#             print(hex_dig)
#             pending_employee_profile = Profile(
#                 name = employee.get('name'),
#                 email = employee.get('email'),
#                 isManager = False,
#                 user_hash = hex_dig
#             )
#             pending_employee_profile.save()
#             pending_employee = Employee(profile=pending_employee_profile)
#             pending_employee.save()
#             #print(pending_employee)

#             team.pending_employees.add(pending_employee)
#             team.save()

#             link = "https://goodneighbordelivery.herokuapp.com/?route=2&code=" + pending_employee_profile.user_hash 
#             print(pending_employee_profile.user_hash, link)
#             message = render_to_string('email.html', {
#                 'employee': pending_employee_profile.name,
#                 'manager': profile_manager.name,
#                 'link': link,
#             })
#             mail_subject = 'Activate your Good Neighbor Account!'
#             to_email = pending_employee_profile.email
#             email = EmailMultiAlternatives(mail_subject, message, to=[to_email])
#             email.content_subtype = 'html'
#             email.mixed_subtype = 'related'
#             email.send()
#     return JsonResponse({'message':'Hello World'})
#     #send each pending employee an email with a link which contains
#     #their signup code
#     #need to fill this out properly/check email integration
#     # message = render_to_string('emails/activate_account.html', {
#     #             'user': ,
#     #             'domain': ,
#     #             'uid': ,
#     #             'token': ,
#     #         })
#     # mail_subject = 'Activate your Good Neighbor Account!'
#     # to_email = data.email
#     # email = EmailMultiAlternatives(mail_subject, message, to=[to_email])
#     # email.content_subtype = 'html'
#     # mail.mixed_subtype = 'related'
#     # email.send()

# @api_view(['PATCH'])
# def onboard_employee(request):
#     #adding employee to their team here by pk of team created
#     #find employee obj based on pk somehow
#     try:
#         profile = Profile.objects.get(user = request.user)
#     except profile.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     print(profile)
#     #get the team object from the employee based on pending list
#     try:
#         employee = Employee.objects.get(profile=profile)
#     except employee.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     print(employee)

#     try:
#         team = employee.pending_employees_list.first()
#     except team.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     print(team)
#     if request.method == 'PATCH':
    
#         serializer = OnboardEmployeeSerializer(profile, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     team.pending_employees.remove(employee)
#     team.employees.add(employee)
#     team.save()
#     return JsonResponse({'message':'Hello World'})


    
#     #used serializer I created for adding employee- how do i know 
#     #if it will add the employee or replace the current ones?
#     # serializer = TeamCreateSerializer(data = employee)
#     # if serializer.is_valid():
#     #         serializer.save()
#     #         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#     # return Response(EmployeeSerializer(employee).data)
# @api_view(['PATCH'])
# def set_team_menu(request, pk):
#     try:
#         team = Team.objects.get(pk=pk)
#     except team.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     if request.method == 'PATCH':
#         serializer = TeamMenuSerializer(team, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# #get for menu items on a specific team's menu
# #returns serialized menu object which contains foodItems and their infos
# #do i need to serialize this menu again lol
# @api_view(['GET'])
# def get_team_menu(request, pk):
#     try:
#         team = Team.objects.get(pk=pk)
#     except team.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     menu = team.get_menu()
#     # response = requests.get('http://localhost:8000/api/menu/' + str(menu.id))
#     # print(response)
#     # todos = response.json()
#     # return todos
#     # print(menu.location)
#     # print(menu.get_foodItems())

#     print(menu)
#     team_menu = Menu.objects.get(pk = menu.pk)
#     print(team_menu)
#     serializer = MenuSerializer(team.get_menu())
#     #print(serializer)
#     # print(serializer.is_valid())
#     # if serializer.is_valid():
#     #     serializer.save()
#     return Response(serializer.data)
#     #return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# #Post to create a user's preference
# @api_view(['POST'])
# def create_preference(request):
#     try:
#         profile = Profile.objects.get(user = request.user)
#     except profile.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)

#     preference_object = Preference(
#         user = profile
#     )
#     preference_object.save()
#     return JsonResponse({'message':'Hello World'})

# #Patch to update a user's Preference 
# #find preference by user id, and then update it??
# @api_view(['GET','PATCH'])
# def choose_meal_preference(request, pk):
#     #should I match the pk of the user & date here, or the pk of just the
#     #Preference obj since it has already been created?
#     if request.method == 'GET':
#         data = PreferenceGetSerializer(request.body).data
#         try:
#             preference = Preference.objects.filter(user=pk, date = data.date).first()

#         except preference.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)
#     #TODO: fix - would this work?
#     if request.method == 'PATCH':
#         try:
#             preference = Preference.objects.filter(pk=pk)

#         except preference.DoesNotExist:
#             return Response(status=status.HTTP_404_NOT_FOUND)

#         serializer = PreferenceChooseSerializer(preference, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    


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
