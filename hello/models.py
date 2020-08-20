from django.db import models

# Create your models here.

class Restaurant(models.Model):
    name = models.CharField(max_length = 100)
    location = models.CharField(max_length = 100)

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

class Employee(models.Model):
    name = models.CharField(max_length = 60)
    email = models.CharField(max_length = 60)
    password = models.CharField(max_length = 60)
    location = models.CharField(max_length = 60) #deliveryAddress
    deliveryMade = models.BooleanField(default=False)
    foodItem=models.ForeignKey(FoodItem, on_delete=models.CASCADE, default = 0)

    def get_foodItem(self):
        return self.foodItem


class Manager(models.Model):
    name = models.CharField(max_length = 60)
    email = models.CharField(max_length = 60)
    password = models.CharField(max_length = 60)
    location = models.CharField(max_length = 60)
    deliveryMade = models.BooleanField(default=False)
    foodItem = models.ForeignKey(FoodItem, on_delete=models.CASCADE, default = 0)

    def get_foodItem(self):
        return self.foodItem
    

class Team(models.Model):
    manager = models.ManyToManyField(Manager)
    employees = models.ManyToManyField(Employee)
    menu =models.ForeignKey(Menu, on_delete=models.CASCADE)

    def get_manager(self):
        return self.manager

    def get_employees(self):
        return self.employees
    
    def get_menu(self):
        return self.menu
    