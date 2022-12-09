from .models import *
from django.shortcuts import redirect , render
import stripe
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render, get_object_or_404
import json

from django.http import HttpResponse, JsonResponse


stripe.api_key = settings.STRIPE_SECRET_KEY


STRIPE_PUBLISHABLE_KEY= settings.STRIPE_PUBLISHABLE_KEY
STRIPE_SECRET_KEY=  settings.STRIPE_SECRET_KEY



###SUBSCRIPTION###
def subscription(request):
   
    if request.method == 'POST':
        pass
    else:
        membership = 'monthly'
        final_inr = 150
        membership_id = 'price_1MCI8eSIeyPpwH6Uubcqlf1J'
        if request.method == 'GET' and 'membership' in request.GET:
            if request.GET['membership'] == 'yearly':
                membership = 'yearly'
                membership_id = 'price_1MCI8eSIeyPpwH6UWirNMVmR'
                final_inr = 1200

        # Create Strip Checkout
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
          
            line_items=[{
                'price': membership_id,
                'quantity': 1,
            }],
            mode='subscription',
            allow_promotion_codes=True,
            success_url='http://127.0.0.1:8000/success?session_id={CHECKOUT_SESSION_ID}',
            cancel_url='http://127.0.0.1:8000/cancel',
        )

        return render(request, 'subscription/subscription.html', {'final_inr': final_inr, 'session_id': session.id})





def premium(request):
    return render( request , 'subscription/premium.html')

def settings(request):
    membership = False
    cancel_at_period_end = False
    if request.method == 'POST':
        subscription = stripe.Subscription.retrieve(request.user.username.stripe_subscription_id)
        subscription.cancel_at_period_end = True
        request.user.username.cancel_at_period_end = True
        cancel_at_period_end = True
        subscription.save()
        request.user.username.save()
    else:
        try:
            if request.user.username.membership:
                membership = True
            if request.user.username.cancel_at_period_end:
                cancel_at_period_end = True
        except Customer.DoesNotExist:
            membership = False
    return render(request, 'subscription/settings.html', {'membership':membership,
    'cancel_at_period_end':cancel_at_period_end})


