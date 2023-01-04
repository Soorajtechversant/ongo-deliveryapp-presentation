from .models import *
from django.shortcuts import redirect , render
import stripe
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import redirect, render, get_object_or_404
import json
from django.urls import reverse
from django.views.generic import TemplateView
from django.http import HttpResponse, JsonResponse
from ongoappfolder.models import MerchantDetails


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
            success_url=request.build_absolute_uri(reverse('subscription:success'))+'?session_id={CHECKOUT_SESSION_ID}',
            cancel_url=request.build_absolute_uri(reverse('subscription:cancel')),
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


class SuccessView(TemplateView):
    template_name = "success.html"

    def get_context_data(self, **kwargs):
        context = super(SuccessView, self).get_context_data(**kwargs)
        merchant = MerchantDetails.objects.get(username__username=self.request.user.username)
        merchant.is_subscribed = True
        merchant.save()
        context['merchant'] = merchant
        return context


class CancelView(TemplateView):
    template_name = "cancel.html"