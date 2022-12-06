from django.urls import path
from . import views
from .views import *





urlpatterns = [
    path('pricing_page/', views.pricing_page, name='pricing_page'),
]