from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Profile(models.Model):
     user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
     #user_hash = models.CharField(max_length = 60)
     name = models.CharField(max_length = 60)
     email = models.EmailField(max_length = 254)
     address = models.CharField(max_length = 60) #deliveryAddress

     def get_name(self):
         return self.name
    
     def get_email(self):
         return self.email

class Restaurant(models.Model):
    name = models.CharField(max_length = 100)
    location = models.CharField(max_length = 100)
    picture_url = models.CharField(max_length = 160)
    #menuItems = models.ManyToManyField(MenuItem, related_name="food_restaurants")
    generic_quota_status = models.BooleanField(default= False)
    quota = models.IntegerField()
    #schedules = models.ManyToManyField(Schedule, related_name="related_restaurant")


class MenuItem(models.Model):
     foodName = models.CharField(max_length=100)
     restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE, related_name="menuItems")
     dietaryRestrictions =  models.CharField(max_length=200)
     picture_url = models.CharField(max_length = 160)
     price = models.FloatField()
     popularity = models.IntegerField()

     def get_restaurant(self):
         return self.restaurant

     def get_dietaryRestrictions(self):
         return self.dietaryRestrictions



class Schedule(models.Model):
    restaurant = models.ForeignKey(Restaurant, on_delete= models.PROTECT, related_name= 'schedules')
    date = models.DateField(auto_now = False, auto_now_add = False)
    specific_quota_status = models.BooleanField(default= False)
    quota = models.IntegerField()
    numOrders = models.IntegerField()
    #orders = modelsrs.ForeignKey(Order, related_name="schedules")



class Order(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name= "orders_of_user")
    restaurant = models.ForeignKey(Restaurant, on_delete=models.PROTECT, related_name= "orders" )
    schedule = models.ForeignKey(Schedule, on_delete=models.PROTECT, related_name= "orders")
    deliveryTime= models.DateTimeField(auto_now= False, auto_now_add= False)
    deliveryMade = models.BooleanField(default=False)
    orderTime = models.DateTimeField(auto_now_add = True)
    location = models.CharField(max_length = 100)
    menuItem=models.ForeignKey(MenuItem, on_delete=models.CASCADE, default = 0)
    pricePaid = models.FloatField()

    def get_menuItem(self):
         return self.menuItem

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
    
