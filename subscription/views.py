from django.shortcuts import render
from djstripe.models import Product

def pricing_page(request):
    return render(request, 'pricing_page.html', {
        'products': Product.objects.all()
    })