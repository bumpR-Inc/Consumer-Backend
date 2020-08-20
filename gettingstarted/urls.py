from django.urls import path, include

from django.contrib import admin
from hello.models import *
from rest_framework import routers 
from hello.views import *

admin.autodiscover()

import hello.views

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

router = routers.DefaultRouter()
router.register(r'api/employees', EmployeeViewSet)
router.register(r'api/restaurant', RestaurantViewSet)
router.register(r'api/foodItem', FoodItemViewSet)
router.register(r'api/menu', MenuViewSet)
router.register(r'api/manager', ManagerViewSet)
router.register(r'api/team', TeamViewSet)



urlpatterns = [
    # path("", hello.views.index, name="index"),
#    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
    path(r'', include(router.urls)),
    path(r'api/', include('rest_framework.urls', namespace='rest_framework'))
    
]
