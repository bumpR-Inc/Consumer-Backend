from django.db import models
from django.contrib.auth.models import User
from datetime import datetime

# Create your models here.
class Profile(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
     #user_hash = models.CharField(max_length = 60)
     name = models.CharField(max_length = 60)
     email = models.EmailField(max_length = 254)
     address = models.CharField(max_length = 60) #deliveryAddress
     #phoneNumber = models.PhoneNumberField(blank=True)
     phoneNumber = models.CharField(max_length = 20, default= "0")

     def get_name(self):
         return self.name
    
     def get_email(self):
         return self.email
         
     def __str__(self):
        return self.name

class Restaurant(models.Model):
    name = models.CharField(max_length = 100)
    location = models.CharField(max_length = 100)
    picture_url = models.CharField(max_length = 160)
    #menuItems = models.ManyToManyField(MenuItem, related_name="food_restaurants")
    generic_quota_status = models.BooleanField(default= False)
    quota = models.IntegerField()
    #schedules = models.ManyToManyField(Schedule, related_name="related_restaurant")
    def __str__(self):
        return self.name

class MenuItem(models.Model):
     foodName = models.CharField(max_length=100)
     description = models.CharField(max_length=250)
     restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE, related_name="menuItems")
     dietaryRestrictions =  models.CharField(max_length=200)
     picture_url = models.CharField(max_length = 160)
     price = models.FloatField()
     popularity = models.IntegerField()

     def get_restaurant(self):
         return self.restaurant

     def get_dietaryRestrictions(self):
         return self.dietaryRestrictions

     def __str__(self):
        return self.foodName + " " + self.restaurant.name


class DeliveryDay(models.Model):
    date = models.DateField(auto_now = False, auto_now_add = False)
    daily_quota_status = models.BooleanField(default= False)
    quota = models.IntegerField()

    def __str__(self):
        return str(self.id)
        #return self.date


class RestaurantDeliveryDay(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete= models.PROTECT, related_name= 'schedules')
    deliveryDay = models.ForeignKey(DeliveryDay, on_delete= models.CASCADE, related_name= 'restaurant_deliveryDays', default= None)
    date = models.DateField(auto_now = False, auto_now_add = False)
    specific_quota_status = models.BooleanField(default= False)
    quota = models.IntegerField()
    #orders = models.ForeignKey(Order, related_name="schedules")

    def __str__(self):
        return self.restaurant.name
        #return str(self.restaurant.name + " " +datetime.strftime(self.date, '%Y-%m-%d'))


class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name= "orders_of_user")
    #restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name= "orders" )
    deliveryDay = models.ForeignKey(DeliveryDay, on_delete=models.PROTECT, related_name= "orders", default=None)
    deliveryTime= models.DateTimeField(auto_now= False, auto_now_add= False)
    deliveryMade = models.BooleanField(default=False)
    orderTime = models.DateTimeField(auto_now_add = True)
    location = models.CharField(max_length = 100)
    order_hash = models.CharField(max_length = 100)
    #menuItem=models.ForeignKey(MenuItem, on_delete=models.CASCADE, default = 0)
    pricePaid = models.FloatField()
    tip = models.FloatField()
    tax = models.FloatField()
    deliveryFee = models.FloatField()


    def __str__(self):
        return self.location + " " + self.user.name
        #return str(self.order_hash + " " + datetime.strftime(self.deliveryTime, '%Y-%m-%d'))



class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name= "order_items")
    menuItem = models.ForeignKey(MenuItem, on_delete = models.PROTECT, related_name="order_items")
    price = models.FloatField()

    def get_menuItem(self):
         return self.menuItem

    def __str__(self):
        return self.menuItem.foodName 


# class Restaurant(models.Model):
#     name = models.CharField(max_length = 100)
#     location = models.CharField(max_length = 100)
#     picture_url = models.CharField(max_length = 160)

#     def get_name(self):
#         return self.name

# class FoodItem(models.Model):
#     foodName = models.CharField(max_length=100)
#     restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE)
#     dietaryRestrictions =  models.CharField(max_length=200)
#     picture_url = models.CharField(max_length = 160)

#     def get_restaurant(self):
#         return self.restaurant

#     def get_dietaryRestrictions(self):
#         return self.dietaryRestrictions
    
# class Menu(models.Model):
#     date = models.CharField(max_length = 100) #change later to DateTimeField
#     location = models.CharField(max_length = 100)  #location (city) that the menu caters 
#     foodItems = models.ManyToManyField(FoodItem)

#     def get_foodItems(self):
#         return self.foodItems

# class Profile(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
#     user_hash = models.CharField(max_length = 60)
#     name = models.CharField(max_length = 60)
#     email = models.CharField(max_length = 60)
#     location = models.CharField(max_length = 60) #deliveryAddress
#     isManager = models.BooleanField(default=False)

#     def get_name(self):
#         return self.name
    
#     def get_email(self):
#         return self.email

#     def get_isManager(self):
#         return self.isManager

#     def validate_employee(self):
#         self.isManager = False
#         self.save()

#     def validate_manager(self):
#         self.isManager = True
#         self.save()


# class Preference(models.Model):
#     user = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name= "preferences_of_user")
#     deliveryMade = models.BooleanField(default=False)
#     foodItem=models.ForeignKey(FoodItem, on_delete=models.CASCADE, default = 0)
#     date = models.DateField(auto_now_add = True)

#     def get_foodItem(self):
#         return self.foodItem

# class Employee(models.Model):
#     profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

#     def get_profile(self):
#         return self.profile

# class Manager(models.Model):
#     profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

#     def get_profile(self):
#         return self.profile

# class Team(models.Model):
#     manager = models.ManyToManyField(Manager)
#     employees = models.ManyToManyField(Employee, related_name= "employees_list")
#     pending_employees = models.ManyToManyField(Employee, related_name= "pending_employees_list")
#     menu = models.ForeignKey(Menu, on_delete=models.CASCADE, blank=True, null = True)
#     monday = models.BooleanField(default=False)
#     tuesday = models.BooleanField(default=False)
#     wednesday = models.BooleanField(default=False)
#     thursday = models.BooleanField(default=False)
#     friday = models.BooleanField(default=False)

#     def get_manager(self):
#         return self.manager

#     def get_employees(self):
#         return self.employees

#     def get_pending_employees(self):
#         return self.pending_employees
    
#     def get_menu(self):
#         return self.menu

#     def get_monday(self):
#         return self.monday
    
