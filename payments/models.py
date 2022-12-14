from django.db import models
from ongoappfolder.models import UserDetails, MerchantDetails
from cart.models import Cart,CartItem
# Create your models here.

class Report(models.Model):
    # user = models.ForeignKey(UserDetails, on_delete=models.CASCADE)
    cart_id = models.ForeignKey(Cart, on_delete=models.CASCADE)
    cart_items = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    hotel = models.ForeignKey(MerchantDetails, on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=3, max_digits=7, default=None)
    purchase_date = models.DateField(auto_now=True)

    class Meta:
        verbose_name_plural = 'Reports'

    def __str__(self):
        return str(self.hotel)