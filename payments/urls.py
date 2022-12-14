from django.urls import path
from . import views
from .views import CancelView, SuccessView

app_name = 'payments'
urlpatterns = [
    path('create-checkout-session/<int:id>', views.CreateCheckoutSessionView.as_view(), name='create-checkout-session'),
    path('cancel/', CancelView.as_view(), name='cancel'),
    path('success/<int:id>', SuccessView.as_view(), name='success'),
]