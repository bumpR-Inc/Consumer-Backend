# serializers.py
from rest_framework import serializers

from .models import *
from .models import Employee
from .models import Restaurant

class EmployeeSerializer(serializers.ModelSerializer):
    profile_info=serializers.SerializerMethodField(read_only=True)

    def get_profile_info(self,obj):
        profile=obj.profile
        serializer=ProfileSerializer(profile)
        return serializer.data

    class Meta:
        model = Employee
        fields = [
            'pk',
            'profile',
            'profile_info'
        ]

class PendingEmployeeInfoSerializer(serializers.Serializer):
    name = models.CharField(max_length = 60)
    email = models.CharField(max_length = 60)



class ProfileSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Employee
        fields = [
            'pk',
            'name',
            'location',
            'email',
            'isManager',
            'authZeroID'
        ]

        
class ManagerSerializer(serializers.ModelSerializer):

    profile_info=serializers.SerializerMethodField(read_only=True)

    def get_profile_info(self,obj):
        profile=obj.profile
        serializer=ProfileSerializer(profile)
        return serializer.data
    
    class Meta:
        model = Manager 
        fields = [
            'pk',
            'profile',
            'profile_info'
            ]
class OnboardManagerSerializer(serializers.Serializer):
    name = models.CharField(max_length = 60)
    email = models.CharField(max_length = 60)
    location = models.CharField(max_length = 100)
    

class OnboardEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = [
            'pk',
            'name',
            'email',
            'location',
            'authZeroID',
        ]

class TeamSerializer(serializers.ModelSerializer):

    menu_info=serializers.SerializerMethodField(read_only=True)
    manager= serializers.PrimaryKeyRelatedField(queryset=Manager.objects.all(), many=True)
    employees= serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), many=True)
    manager_info=serializers.SerializerMethodField(read_only=True)
    employees_info=serializers.SerializerMethodField(read_only=True)

    def get_menu_info(self,obj):
        menu=obj.menu
        serializer=MenuSerializer(menu)
        return serializer.data

    def get_manager_info(self, obj):
        response = []
        manager = obj.manager
        for m in manager.all():
            serializer = ManagerSerializer(m)
            response += [serializer.data]
        return response

    def get_employees_info(self, obj):
        response = []
        employees = obj.employees
        for employee in employees.all():
            serializer = EmployeeSerializer(employee)
            response += [serializer.data]
        return response
    
    class Meta:
        model = Team
        fields = [
            'pk',
            'manager',#ManytoMany
            'employees', #ManytoMany
            'pending_employees',#ManytoMany
            'menu',#ForeignKey
            'menu_info',
            'manager_info',
            'employees_info',
            'monday',
            'tuesday',
            'wednesday',
            'thursday',
            'friday',
        ]

class TeamCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'pk',
            'employees',
        ]
            
class TeamRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'pk',
            'pending_employees',
        ]

class TeamScheduleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = [
            'pk',
            'monday',
            'tuesday',
            'wednesday',
            'thursday',
            'friday',
        ]

class PreferenceSerializer(serializers.ModelSerializer):
    foodItem_info=serializers.SerializerMethodField(read_only=True)

    def get_fooditem_info(self,obj):
        foodItem=obj.foodItem
        serializer=FoodItemSerializer(foodItem)
        return serializer.data

    class Meta:
        model = Preference
        fields = [
            'pk',
            'user',
            'deliveryMade',
            'foodItem',
            'foodItem_info',
            'date',
        ]
class PreferenceGetSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preference
        fields = [
            'pk',
            'date',
        ]

class PreferenceChooseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Preference
        fields = [
            'pk',
            'foodItem',
            'date',
        ]

class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = [
            'pk',
            'name',
            'location',
            'picture_url',
        ]
        
class FoodItemSerializer(serializers.ModelSerializer):

    restaurant_info=serializers.SerializerMethodField(read_only=True)
    

    def get_restaurant_info(self,obj):
        restaurant=obj.restaurant
        serializer=RestaurantSerializer(restaurant)
        return serializer.data

    class Meta:
        model = FoodItem
        fields = [
            'pk',
            'foodName',
            'restaurant',#ForeignKey
            'restaurant_info',
            'dietaryRestrictions',
            'picture_url',
        ]

        

class MenuSerializer(serializers.ModelSerializer):


    foodItems= serializers.PrimaryKeyRelatedField(queryset=FoodItem.objects.all(), many=True)
    foodItems_info=serializers.SerializerMethodField(read_only=True)

    def get_foodItems_info(self, obj):
        response = []
        foodItems = obj.foodItems
        for foodItem in foodItems.all():
            serializer = FoodItemSerializer(foodItem)
            response += [serializer.data]
        return response

    class Meta:
        model = Menu 
        fields = [
            'pk',
            'date',
            'location',
            'foodItems', #ManytoMany
            'foodItems_info',
            ]

