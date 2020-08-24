from django.db import models

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length = 100)
    location = models.CharField(max_length = 100)

    def get_name(self):
        return self.name

class FoodItem(models.Model):
    foodName = models.CharField(max_length=100)
    restaurant = models.ForeignKey(Restaurant, on_delete = models.CASCADE)
    dietaryRestrictions =  models.CharField(max_length=200)

    def get_restaurant(self):
        return self.restaurant

    def get_dietaryRestrictions(self):
        return self.dietaryRestrictions
    
class Menu(models.Model):
    date = models.CharField(max_length = 100) #change later to DateTimeField
    location = models.CharField(max_length = 100)  #location (city) that the menu caters 
    foodItems = models.ManyToManyField(FoodItem)

    def get_foodItems(self):
        return self.foodItems

class Profile(models.Model):
    name = models.CharField(max_length = 60)
    email = models.CharField(max_length = 60)
    location = models.CharField(max_length = 60) #deliveryAddress
    isManager = models.BooleanField(default=False)
    authZeroID = models.CharField(max_length = 60)

class Preference(models.Model):
    user = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name= "preferences_of_user")
    deliveryMade = models.BooleanField(default=False)
    foodItem=models.ForeignKey(FoodItem, on_delete=models.CASCADE, default = 0)
    date = models.DateField(auto_now_add = True)

    def get_foodItem(self):
        return self.foodItem

class Employee(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def get_profile(self):
        return self.profile

class Manager(models.Model):
    profile = models.OneToOneField(Profile, on_delete=models.CASCADE)

    def get_profile(self):
        return self.profile


class Team(models.Model):
    manager = models.ManyToManyField(Manager)
    employees = models.ManyToManyField(Employee)
    menu =models.ForeignKey(Menu, on_delete=models.CASCADE)
    monday = models.BooleanField(default=False)
    tuesday = models.BooleanField(default=False)
    wednesday = models.BooleanField(default=False)
    thursday = models.BooleanField(default=False)
    friday = models.BooleanField(default=False)

    def get_manager(self):
        return self.manager

    def get_employees(self):
        return self.employees
    
    def get_menu(self):
        return self.menu

    def get_monday(self):
        return self.monday
    