from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from ongoappfolder.models import *
# Create your views here.
from chat.models import Thread


@login_required
def messages_page(request):
    threads = Thread.objects.by_user(user=request.user).prefetch_related('chatmessage_thread').order_by('timestamp')
    
    context = {
        'Threads': threads,
        'hotel': HotelName.objects.all(),
        'data': UserDetails.objects.get(username__username=request.user.username)
    }
    return render(request, 'messages.html', context)
context = {
                
            }
