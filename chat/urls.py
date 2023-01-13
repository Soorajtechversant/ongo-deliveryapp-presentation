

from django.urls import path
from . import views

app_name = "chat" 


urlpatterns = [
    path('create-chat/', views.Chat, name="create_chat"),
    path('<id>/', views.messages_page, name="messages"),



]
