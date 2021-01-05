from django.urls import path, include

from django.contrib import admin
from hello.models import *
from rest_framework import routers 
from hello.views import *

admin.autodiscover()

import hello.views

from hello import views

from rest_framework.authtoken import views as auth_views

from django.views.decorators.csrf import csrf_exempt
# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

router = routers.DefaultRouter()
router.register(r'api/users', UserViewSet)
router.register(r'api/profiles', ProfileViewSet)
router.register(r'api/restaurants', RestaurantViewSet)
router.register(r'api/menuItems', MenuItemSet)
router.register(r'api/orders', OrderViewSet)

# router.register(r'api/employees', EmployeeViewSet)
# router.register(r'api/restaurant', RestaurantViewSet)
# router.register(r'api/foodItem', FoodItemViewSet)
# router.register(r'api/menu', MenuViewSet)
# router.register(r'api/manager', ManagerViewSet)
# router.register(r'api/team', TeamViewSet)
# router.register(r'api/profile', ProfileViewSet)
# router.register(r'api/preferences', PreferenceViewSet)
# router.register(r'api/user', UserViewSet, base_name ='user_api')
#adding all more in depth apis here

#router.register(r'^api/public/', views.public)
#router.register(r'^api/private/', views.private)

urlpatterns = [
    # path("", hello.views.index, name="index"),
#    path("db/", hello.views.db, name="db"),

    #path("admin/", admin.site.urls),
    path(r'', include(router.urls)),
    #path(r'api/', include('rest_framework.urls', namespace='rest_framework')),
    
    path('api/public', views.public),
    path('api/private', views.private),
    path('api/private-scoped', views.private_scoped),
    path('api/profilesedit', views.ProfileDetail, name ='profilesedit'),
    path('api/restaurantsedit', csrf_exempt(views.RestaurantDetail.as_view()), name ='restaurantsedit'),
    path('api/restaurantscreate', csrf_exempt(views.RestaurantCreate.as_view()), name ='restaurantscreate'),
    path('api/<int:pk>/menuItemsedit', csrf_exempt(views.MenuItemDetail.as_view()), name = 'menuItemsedit'),
    path('api/menuItemscreate', csrf_exempt(views.MenuItemCreate.as_view()), name ='menuItemscreate'),
    path('api/ordersedit', views.OrderDetail, name = 'ordersedit'),


    # path(r'api/fooditem/<int:pk>/',views.FoodItemDetail.as_view(), name='foodItem_detail_view'),
    # path(r'api/team/<int:pk>/schedule',views.team_schedule, name='team_schedule_view'),
    # #path(r'api/manager/authorization', views.manager_auth, name= 'manager_authorization'),
    # path(r'api/employee/<user_hash>/auth', views.employee_auth, name= 'employee_auth'),
    # path(r'api/manager/onboard', views.onboard_manager, name='onboard_manager'),
    # path(r'api/team/<int:pk>/pending-employees', views.add_pending_employee, name='add_employees'),
    # path(r'api/employee/onboard', views.onboard_employee, name= 'onboard_employee'),
    # path(r'api/team/<int:pk>/menu', views.get_team_menu, name='team_menu_view'),
    # path(r'api/team/<int:pk>/set-menu', views.set_team_menu, name='team_menu_set'),
    # path(r'api/employee/<int:pk>/meal-preference', views.choose_meal_preference, name='choose_meal_preference'),
    # path(r'api/team/<int:pk>/menu', views.get_team_menu, name='team_menu_view'),
    # path(r'api/preferences/create', views.create_preference, name= 'create_preference'),
    # path(r'api/email-test', views.email_test, name= 'email_test'),



    # path(r'api/public',views.public, name='public_test'),
    # path(r'api/manager/auth', views.manager_auth, name= 'manager_auth'),

    # path(r'api/private',views.private, name='private_test'),
    # path('api-token-auth',auth_views.obtain_auth_token, name='api-token-auth'),
    # path('email-preview', views.email_preview, name='email-preview')
    #path(r'api/index', views.index),
    #path('dashboard', views.dashboard),
    #path('logout', views.logout),
    #path('', include('django.contrib.auth.urls')),
    #path('', include('social_django.urls')),

]
