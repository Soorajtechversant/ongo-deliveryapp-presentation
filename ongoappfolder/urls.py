from django.urls import path
from . import views
from .views import *



urlpatterns = [
    
    
    #Customer Urls
    path('',views.Customer_index.as_view(),name="customer_index" , ),
    path('registration',CustomerRegistration.as_view(),name="registration"),

    #Merchant Urls
    path('merchantregistration',MerchantRegistration.as_view(),name="merchantregistration"),
    path('auth/login/',Login.as_view(),name="login"),
    path('owner_index/',Owner_index.as_view(),name="owner_index"),
    path('add_product/',Add_product.as_view(),name="add_product"),
    path('edit_product/<int:id>/',Edit_product.as_view(),name="edit_product"),
    path('Delete_product/<int:id>',Delete_product.as_view(),name="Delete_product"),
    path('detail/<id>/', ProductDetailView.as_view(), name='detail'),
   
    #Common Urls
    path('logout/',Logout.as_view(),name="logout"),
    path('auth/settings', views.settings, name='settings'),
    path('profile/',CustomerProfile.as_view(),name="profile"),   
    path('about/', About.as_view(), name='about'),
    path('services/', Services.as_view(), name='services'),
    path('contact/', Contact.as_view(), name='contact'),


    #Admin Urls
    path('approvals/',MerchantApprovalIndex.as_view(),name="approvals"),
    path('merchant-approvals/<int:id>',MerchantApproval.as_view(),name="approve_merchant"),
    path('hotelproducts/<name>', HotelProducts.as_view(), name='hotelproducts'),

    path('searchtitles/',searchtitles,name="searchtitles"),
    
    #forgot password urls
    path('forgot-password/generate-otp/', GenerateOTP.as_view(), name='generate_otp'),
    path('forgot-password/verify-otp/<int:id>', VerifyOTP.as_view(), name='verify_otp'),
    path('forgot-password/change/<int:id>', ForgotPasswordChange.as_view(), name='forgot_password'),
    
]