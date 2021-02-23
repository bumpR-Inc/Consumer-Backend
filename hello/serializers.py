# serializers.py
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


class MenuItemSerializer(serializers.ModelSerializer):

    restaurant_info=serializers.SerializerMethodField(read_only=True)
    

    def get_restaurant_info(self,obj):
        restaurant=obj.restaurant
        serializer=RestaurantSerializer(restaurant)
        return serializer.data

    class Meta:
        model = MenuItem
        fields = [
            'pk',
            'foodName',
            'description',
            'restaurant',#ForeignKey
            'restaurant_info',
            'dietaryRestrictions',
            'picture_url',
            'price',
            'popularity',
        ]

class OrderSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField(read_only=True)
    

    def get_user_info(self,obj):
        user=obj.user
        serializer=ProfileSerializer(user)
        return serializer.data


    class Meta:
        model = Order
        fields = [
            'pk',
            'user',
            'user_info',
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

class OrderWithItemsSerializer(serializers.ModelSerializer):
    user_info = serializers.SerializerMethodField(read_only=True)
    items_info = serializers.SerializerMethodField(read_only=True)
    

    def get_user_info(self,obj):
        user=obj.user
        serializer=ProfileSerializer(user)
        return serializer.data

    def get_items_info(self,obj):
        items = OrderItem.objects.filter(order=obj)
        item_data = [OrderItemSerializer(item).data for item in items]
        # user=obj.user
        # serializer=ProfileSerializer(user)
        return item_data

    class Meta:
        model = Order
        fields = [
            'pk',
            'user',
            'user_info',
            "deliveryDay",
            'deliveryTime',
            'deliveryMade',
            'orderTime',
            'location',
            'pricePaid',
            'items_info',
            'tip',
            'tax',
            'deliveryFee',
        ]

class OrderCreateSerializer(serializers.Serializer):
    #restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name= "orders" )
    deliveryTime= models.DateTimeField(auto_now= False, auto_now_add= False)
    location = models.CharField(max_length = 100)
    order_hash = models.CharField(max_length = 100)
    #menuItem=models.ForeignKey(MenuItem, on_delete=models.CASCADE, default = 0)
    menuItems =serializers.ListField(child=serializers.IntegerField())
    pricePaid = models.FloatField()
    tip = models.FloatField()
    tax = models.FloatField()
    deliveryFee = models.FloatField()

class OrderPriceCheckerSerializer(serializers.Serializer):
    menuItems =serializers.ListField(child=serializers.IntegerField())

# class OrderPriceEstimateSerializer(serializers.Serializer):
#     orderItemsTotal = models.FloatField()
#     tax = models.FloatField()
#     deliveryFee = models.FloatField()

class OrderItemSerializer(serializers.ModelSerializer):
    menuItem_info = serializers.SerializerMethodField(read_only=True)
    order_info = serializers.SerializerMethodField(read_only=True)


    def get_menuItem_info(self,obj):
        menuItem=obj.menuItem
        serializer=MenuItemSerializer(menuItem)
        return serializer.data

    def get_order_info(self,obj):
         order=obj.order
         serializer=OrderSerializer(order)
         return serializer.data

    class Meta: 
        model = OrderItem 
        fields = [
            'pk',
            'menuItem',
            'menuItem_info',
            'order',
            'order_info',
            'price',
        ]

class OrderItemWithOrderSerializer(serializers.ModelSerializer):
    menuItem_info = serializers.SerializerMethodField(read_only=True)
    order_info = serializers.SerializerMethodField(read_only=True)

    def get_menuItem_info(self,obj):
        menuItem=obj.menuItem
        serializer=MenuItemSerializer(menuItem)
        return serializer.data

    def get_order_info(self,obj):
        order=obj.order
        serializer=OrderSerializer(order)
        return serializer.data
    

    class Meta: 
        model = OrderItem 
        fields = [
            'pk',
            'menuItem',
            'menuItem_info',
            'order',
            'order_info',
            'price',
        ]


# class EmployeeSerializer(serializers.ModelSerializer):
#     profile_info=serializers.SerializerMethodField(read_only=True)

#     def get_profile_info(self,obj):
#         profile=obj.profile
#         serializer=ProfileSerializer(profile)
#         return serializer.data

#     class Meta:
#         model = Employee
#         fields = [
#             'pk',
#             'profile',
#             'profile_info'
#         ]

# # class PendingEmployeeInfoSerializer(serializers.Serializer):
# #     name = models.CharField(max_length = 60)
# #     email = models.CharField(max_length = 60)

# class PendingEmployeeInfoSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Profile
#         fields = [
#             'name',
#             'email',
#         ]

# class ProfileSerializer(serializers.ModelSerializer):
    
#     class Meta:
#         model = Profile
#         fields = [
#             'pk',
#             'user',
#             'user_hash',
#             'name',
#             'location',
#             'email',
#             'isManager',
#         ]

        
# class ManagerSerializer(serializers.ModelSerializer):

#     profile_info=serializers.SerializerMethodField(read_only=True)

#     def get_profile_info(self,obj):
#         profile=obj.profile
#         serializer=ProfileSerializer(profile)
#         return serializer.data
    
#     class Meta:
#         model = Manager 
#         fields = [
#             'pk',
#             'profile',
#             'profile_info',
#             ]
            
# class OnboardManagerSerializer(serializers.Serializer):
#     name = models.CharField(max_length = 60)
#     email = models.CharField(max_length = 60)
#     location = models.CharField(max_length = 100)
    

# class OnboardEmployeeSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Profile
#         fields = [
#             'pk',
#             'name',
#             'email',
#             'location',
#         ]

# class TeamSerializer(serializers.ModelSerializer):

#     menu_info=serializers.SerializerMethodField(read_only=True)
#     manager= serializers.PrimaryKeyRelatedField(queryset=Manager.objects.all(), many=True)
#     employees= serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), many=True)
#     manager_info=serializers.SerializerMethodField(read_only=True)
#     employees_info=serializers.SerializerMethodField(read_only=True)

#     def get_menu_info(self,obj):
#         menu=obj.menu
#         serializer=MenuSerializer(menu)
#         return serializer.data

#     def get_manager_info(self, obj):
#         response = []
#         manager = obj.manager
#         for m in manager.all():
#             serializer = ManagerSerializer(m)
#             response += [serializer.data]
#         return response

#     def get_employees_info(self, obj):
#         response = []
#         employees = obj.employees
#         for employee in employees.all():
#             serializer = EmployeeSerializer(employee)
#             response += [serializer.data]
#         return response
    
#     class Meta:
#         model = Team
#         fields = [
#             'pk',
#             'manager',#ManytoMany
#             'employees', #ManytoMany
#             'pending_employees',#ManytoMany
#             'menu',#ForeignKey
#             'menu_info',
#             'manager_info',
#             'employees_info',
#             'monday',
#             'tuesday',
#             'wednesday',
#             'thursday',
#             'friday',
#         ]

# class TeamCreateSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Team
#         fields = [
#             'pk',
#             'employees',
#         ]
            
# class TeamRegisterSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Team
#         fields = [
#             'pk',
#             'pending_employees',
#         ]

# class TeamScheduleSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Team
#         fields = [
#             'pk',
#             'monday',
#             'tuesday',
#             'wednesday',
#             'thursday',
#             'friday',
#         ]
# class TeamMenuSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = Team
#         fields = [
#             'pk',
#             'menu',
#         ]

# class PreferenceSerializer(serializers.ModelSerializer):
#     foodItem_info=serializers.SerializerMethodField(read_only=True)

#     def get_fooditem_info(self,obj):
#         foodItem=obj.foodItem
#         serializer=FoodItemSerializer(foodItem)
#         return serializer.data

#     class Meta:
#         model = Preference
#         fields = [
#             'pk',
#             'user',
#             'deliveryMade',
#             'foodItem',
#             'foodItem_info',
#             'date',
#         ]
# class PreferenceGetSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Preference
#         fields = [
#             'pk',
#             'date',
#         ]

# class PreferenceChooseSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Preference
#         fields = [
#             'pk',
#             'foodItem',
#             'date',
#         ]

# class RestaurantSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = Restaurant
#         fields = [
#             'pk',
#             'name',
#             'location',
#             'picture_url',
#         ]
        
# class FoodItemSerializer(serializers.ModelSerializer):

#     restaurant_info=serializers.SerializerMethodField(read_only=True)
    

#     def get_restaurant_info(self,obj):
#         restaurant=obj.restaurant
#         serializer=RestaurantSerializer(restaurant)
#         return serializer.data

#     class Meta:
#         model = FoodItem
#         fields = [
#             'pk',
#             'foodName',
#             'restaurant',#ForeignKey
#             'restaurant_info',
#             'dietaryRestrictions',
#             'picture_url',
#         ]

        

# class MenuSerializer(serializers.ModelSerializer):


#     foodItems= serializers.PrimaryKeyRelatedField(queryset=FoodItem.objects.all(), many=True)
#     foodItems_info=serializers.SerializerMethodField(read_only=True)

#     def get_foodItems_info(self, obj):
#         response = []
#         foodItems = obj.foodItems
#         for foodItem in foodItems.all():
#             serializer = FoodItemSerializer(foodItem)
#             response += [serializer.data]
#         return response

#     class Meta:
#         model = Menu 
#         fields = [
#             'pk',
#             'date',
#             'location',
#             'foodItems', #ManytoMany
#             'foodItems_info',
#             ]

