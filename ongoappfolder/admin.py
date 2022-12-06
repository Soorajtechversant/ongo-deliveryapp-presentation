from django.contrib import admin
from .models import HotelName, UserLoginDetails,UserDetails,MerchantDetails
# Register your models here.

admin.site.register(HotelName)
admin.site.register(UserDetails)
admin.site.register(MerchantDetails)
admin.site.register(UserLoginDetails)
