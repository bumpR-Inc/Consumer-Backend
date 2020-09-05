from django.urls import path, include

from django.contrib import admin
from hello.models import *
from rest_framework import routers 
from hello.views import *

admin.autodiscover()

import hello.views

from hello import views

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
router.register(r'api/user', UserViewSet, base_name ='user_api')
#router.register(r'^api/public/', views.public)
#router.register(r'^api/private/', views.private)

urlpatterns = [
    # path("", hello.views.index, name="index"),
#    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls),
    path(r'', include(router.urls)),
    path(r'api/', include('rest_framework.urls', namespace='rest_framework')),
    #path(r'api/public/', views.public),
    #path(r'api/private/', views.private),
    path(r'api/fooditem/<int:pk>/',views.FoodItemDetail.as_view(), name='foodItem_detail_view'),
    path(r'api/team/<int:pk>/schedule',views.team_schedule, name='team_schedule_view'),
    path(r'api/public',views.public, name='public_test'),
    path(r'api/private',views.private, name='private_test'),
    #path(r'api/index', views.index),
    #path('dashboard', views.dashboard),
    #path('logout', views.logout),
    #path('', include('django.contrib.auth.urls')),
    #path('', include('social_django.urls')),

]
