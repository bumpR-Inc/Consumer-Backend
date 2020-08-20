# serializers.py
from rest_framework import serializers

from .models import *
from .models import Employee
from .models import Restaurant

class EmployeeSerializer(serializers.ModelSerializer):

    foodItem_info=serializers.SerializerMethodField(read_only=True)

    def get_foodItem_info(self,obj):
        foodItem=obj.foodItem
        serializer=FoodItemSerializer(foodItem)
        return serializer.data
   
    class Meta:
        model = Employee
        fields = [
            'pk',
            'name',
            'location',
            'email',
            'password',
            'deliveryMade',
            'foodItem', #ForeignKey
            'foodItem_info'
        ]
        
class ManagerSerializer(serializers.ModelSerializer):

    foodItem_info=serializers.SerializerMethodField(read_only=True)

    def get_foodItem_info(self,obj):
        foodItem=obj.foodItem
        serializer=FoodItemSerializer(foodItem)
        return serializer.data
    
    class Meta:
        model = Manager 
        fields = [
            'pk',
            'name',
            'location',
            'email',
            'password',
            'deliveryMade',
            'foodItem', #ForeignKey
            'foodItem_info'
            ]

class TeamSerializer(serializers.ModelSerializer):

    menu_info=serializers.SerializerMethodField(read_only=True)

    def get_menu_info(self,obj):
        menu=obj.menu
        serializer=MenuSerializer(menu)
        return serializer.data
    
    class Meta:
        model = Team
        fields = [
            'pk',
            'manager',#ManytoMany
            'employees', #ManytoMany
            'menu',#ForeignKey
            'menu_info',
        ]
            
class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = [
            'pk',
            'name',
            'location',
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
        ]

        

class MenuSerializer(serializers.ModelSerializer):


    #foodItems= serializers.PrimaryKeyRelatedField(queryset=FoodItem.objects.all(), many=True)
    foodItems = FoodItemSerializer(many = True, read_only=True)

    class Meta:
        model = Menu 
        fields = [
            'pk',
            'date',
            'location',
            'foodItems', #ManytoMany
            ]

