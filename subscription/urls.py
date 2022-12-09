from django.urls import path
from . import views
from .views import *





urlpatterns = [
  
    path('subscription/',views.subscription,name='subscription'), 
    path('premium',views.premium,name='premium'), 
    path('auth/settings', views.settings, name='settings'),


]