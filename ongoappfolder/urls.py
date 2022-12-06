from django.urls import path
from . import views
from .views import *



urlpatterns = [

    path('',views.Index.as_view(),name="index"),
    path('customer_index/',views.Customer_index.as_view(),name="customer_index"),
    path('registration',CustomerRegistration.as_view(),name="registration"),
    path('merchantregistration',MerchantRegistration.as_view(),name="merchantregistration"),
    path('auth/login/',Login.as_view(),name="login"),
    path('logout/',Logout.as_view(),name="logout"),
    path('auth/settings', views.settings, name='settings'),
    path('profile/',CustomerProfile.as_view(),name="profile"),


    path('owner_index/',Owner_index.as_view(),name="owner_index"),
    path('add_product/',Add_product.as_view(),name="add_product"),
    path('approvals/',MerchantApprovalIndex.as_view(),name="approvals"),
    path('merchant-approvals/<int:id>',MerchantApproval.as_view(),name="approve_merchant"),
    path('edit_product/<int:id>/',Edit_product.as_view(),name="edit_product"),
    path('Delete_product/<int:id>',Delete_product.as_view(),name="Delete_product"),
   
    path('customer_index/',Customer_index.as_view(),name="customer_index"),
    path('hotelproducts/<name>', HotelProducts.as_view(), name='hotelproducts'),

    path('detail/<id>/', ProductDetailView.as_view(), name='detail'),
    

    
]