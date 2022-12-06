from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from distutils.command.upload import upload
from django.db import models

class UserLoginDetails(AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255,blank=True)
    last_name = models.CharField(max_length=255,blank=True)
    email = models.CharField(max_length=255,blank=True)
    address = models.CharField(max_length=255,blank=True)
    phn_number = models.CharField(max_length=255,blank=True)
    password = models.CharField(max_length=255,blank=True)
    user_type = models.CharField(max_length=255,blank=True)
    

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = "UserLoginDetail"
        verbose_name_plural = "UserLoginDetails"

class MerchantDetails(models.Model):
    username = models.ForeignKey(UserLoginDetails, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255,blank=True)
    last_name = models.CharField(max_length=255,blank=True)
    email = models.CharField(max_length=255,blank=True)
    address = models.CharField(max_length=255,blank=True)
    phn_number = models.CharField(max_length=255,blank=True)
    profile_pic = models.FileField(upload_to="profile_pic/")
    hotel_name = models.CharField(max_length=255,blank=True)
    bussiness_type = models.CharField(max_length=255,blank=True)
    is_approved = models.BooleanField(default=False)

    def __str__(self):
        return self.first_name

class UserDetails(models.Model):
    username = models.ForeignKey(UserLoginDetails, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=255,blank=True)
    last_name = models.CharField(max_length=255,blank=True)
    email = models.CharField(max_length=255,blank=True)
    address = models.CharField(max_length=255,blank=True)
    phn_number = models.CharField(max_length=255,blank=True)
    profile_pic = models.FileField(upload_to="profile_pic/",blank=True, null=True)
   

    def __str__(self):
        return self.first_name


class Customer(models.Model):
    user = models.ForeignKey(UserLoginDetails, on_delete=models.CASCADE)
    # user = models.ForeignKey(User, on_delete=models.CASCADE)

    stripeid = models.CharField(max_length=255)
    stripe_subscription_id = models.CharField(max_length=255)
    cancel_at_period_end = models.BooleanField(default=False)
    membership = models.BooleanField(default=False)




class HotelName(models.Model):
    owner = models.ForeignKey(MerchantDetails, on_delete=models.CASCADE, null=True, blank=True)
    hotelname = models.CharField(max_length=50)
    food = models.CharField(max_length=50)
    ingredients = models.CharField(max_length=50)
    price = models.IntegerField()
    # hotelimage = models.ImageField(upload_to= 'media',null=True,blank=True)
    hotelimage = models.ImageField(upload_to= 'media/hotel',null=True,blank=True)
    productpicture = models.ImageField(upload_to = 'media',null=True,blank = True)

    def __str__(self):
        return self.hotelname





