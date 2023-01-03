from django.contrib.auth.decorators import login_required

from django.shortcuts import render
from ongoappfolder.models import *

from django.shortcuts import render,redirect


# Create your views here.
from chat.models import Thread
from ongoappfolder.models import MerchantDetails, UserDetails, UserLoginDetails,HotelName


@login_required
def messages_page(request, id):
    if request.user.user_type == 'customer' or request.user.is_staff:
        second_person = MerchantDetails.objects.get(id=id)
        data = UserDetails.objects.get(username__username=request.user.username)
        second_person = UserLoginDetails.objects.get(username=second_person.username)
        first_person = request.user
        try:
            temporary = Thread.objects.get(first_person=request.user, second_person=second_person)
        except:
            Thread.objects.create(first_person=first_person, second_person=second_person)
    else:
        first_person = UserDetails.objects.get(id=id)
        data = MerchantDetails.objects.get(username__username=request.user.username)
        first_person = UserLoginDetails.objects.get(username=first_person.username)
        second_person = request.user
        try:
            temporary = Thread.objects.get(first_person=first_person, second_person=request.user)
        except:
            Thread.objects.create(first_person=first_person, second_person=second_person)

    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')

    context = {
        'Threads': threads,
        'hotel': HotelName.objects.all(),
        'data': data
    }
    return render(request, 'messages.html', context)


@login_required
def Chat(request):

    if request.user.user_type == 'customer' or request.user.is_staff:
        merchants = MerchantDetails.objects.all()
        context = {
            'merchants': merchants,
            'data': UserDetails.objects.get(username__username=request.user.username)
        }
    else:
        customers = UserDetails.objects.all()
        context = {
            'merchants': customers,
            'data': MerchantDetails.objects.get(username__username=request.user.username)
        }
    return render(request, 'chat.html', context)

