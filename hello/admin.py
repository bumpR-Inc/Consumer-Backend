from django.contrib import admin

from .models import *
from .models import Restaurant
# Register your models here.
admin.site.register(Employee)
admin.site.register(Restaurant)
admin.site.register(FoodItem)
admin.site.register(Menu)
