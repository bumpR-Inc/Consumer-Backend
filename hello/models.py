from django.db import models

# Create your models here.
class Employee(models.Model):
    email = models.CharField(max_length = 60)
    password = models.CharField(max_length = 60)
    location = models.CharField(max_length = 60)
   # delivery_made = models.BooledsanField(default = False) 
    