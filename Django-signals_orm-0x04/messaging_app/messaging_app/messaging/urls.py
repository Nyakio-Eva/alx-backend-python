from django.urls import path
from .views import delete_user, message_list

urlpatterns = [
    path('messages/', message_list, name='message_list'),
    path('delete-account/', delete_user, name='delete_user'),
]

