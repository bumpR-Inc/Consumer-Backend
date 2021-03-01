from rest_framework import serializers
from django.contrib.auth.models import User
from .models import *

class UserSerializer(serializers.ModelSerializer): 
  
     class Meta: 
         model = User 
         fields =  '__all__'

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = [
            'pk',
            'user',
            'name',
            'email',
            'address',
            'phoneNumber',
        ]

class RestaurantSerializer(serializers.ModelSerializer):

    class Meta:
        model = Restaurant
        fields = [
            'pk',
            'name',
            'location',
            'picture_url',
            'generic_quota_status',
            'quota',
        ]

class DeliveryDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = DeliveryDay
        fields = [
            'pk',
            'date',
            'daily_quota_status',
            'quota',
        ]

class RestaurantDeliveryDaySerializer(serializers.ModelSerializer):

    class Meta:
        model = RestaurantDeliveryDay
        fields = [
            'pk',
            'restaurant',
            'deliveryDay', 
            'date',
            'specific_quota_status',
            'quota',
        ]

class AddInSerializer(serializers.ModelSerializer):
    class Meta:
        model = AddIn
        fields = [
            'pk',
            'name',
            'price',
            'menuItems',
            'orderItems'
        ]

class MenuItemSerializer(serializers.ModelSerializer):
    restaurant = RestaurantSerializer()
    add_ins = AddInSerializer(many=True)

    class Meta:
        model = MenuItem
        fields = [
            'pk',
            'foodName',
            'description',
            'restaurant',
            'dietaryRestrictions',
            'picture_url',
            'price',
            'popularity',
            'add_ins'
        ]

class OrderItemSerializer(serializers.ModelSerializer):
    menuItem = MenuItemSerializer()
    add_ins = AddInSerializer(many=True)
    # order = OrderSerializer()
    user_info = serializers.SerializerMethodField()

    def get_user_info(self, obj):
        return ProfileSerializer(obj.order.user).data

    class Meta: 
        model = OrderItem 
        fields = [
            'pk',
            'menuItem',
            'order',
            'price',
            'add_ins',
            'user_info'
        ]

class OrderSerializer(serializers.ModelSerializer):
    user = ProfileSerializer()
    order_items = OrderItemSerializer(many=True)

    class Meta:
        model = Order
        fields = [
            'pk',
            'user',
            'order_items',
            "deliveryDay",
            'deliveryTime',
            'deliveryMade',
            'orderTime',
            'location',
            'order_hash',
            'pricePaid',
            'tip',
            'tax',
            'deliveryFee',
        ]

class OrderItemCreateSerializer(serializers.Serializer):
    menuItem = serializers.IntegerField()
    addIns = serializers.ListField(child=serializers.IntegerField())

class OrderCreateSerializer(serializers.Serializer):
    deliveryTime= models.DateTimeField(auto_now= False, auto_now_add= False)
    location = models.CharField(max_length = 100)
    order_hash = models.CharField(max_length = 100)
    menuItems = OrderItemCreateSerializer(many=True)
    pricePaid = models.FloatField()
    tip = models.FloatField()
    tax = models.FloatField()
    deliveryFee = models.FloatField()

class OrderPriceCheckerSerializer(serializers.Serializer):
    menuItems = serializers.ListField(child=serializers.IntegerField())