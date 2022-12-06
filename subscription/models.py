from django.db import models

# Create your models here.




class MyStripeModel(models.Model):
    name = models.CharField(max_length=100)
    stripe_subscription_id = models.CharField(max_length=100)