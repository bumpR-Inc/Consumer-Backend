from django.contrib import admin

from .models import *

# Register your models here.
admin.site.register(Profile)
admin.site.register(Restaurant)
admin.site.register(MenuItem)
admin.site.register(Order)
admin.site.register(DeliveryDay)
admin.site.register(RestaurantDeliveryDay)
admin.site.register(OrderItem)
