from django.conf import settings
from django.contrib import admin
from django.urls import path , include
from django.contrib.staticfiles.urls import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('ongoappfolder.urls' )),
    path('subscription',include('subscription.urls')),
    path('cart',include('cart.urls' )),
    path('payments/',include('payments.urls' )),
    path('chat/', include('chat.urls')),
    path('search/', include('haystack.urls')),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)#For serving uploaded files