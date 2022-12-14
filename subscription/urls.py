from django.urls import path
from . import views
from .views import *




app_name = 'subscription'

urlpatterns = [
  
    path('subscription/',views.subscription,name='subscription'), 
    path('premium',views.premium,name='premium'), 
    path('auth/settings', views.settings, name='settings'),
    path('cancel/$', CancelView.as_view(), name='cancel'),
    path('success/$', SuccessView.as_view(), name='success'),


]