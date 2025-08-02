from django.shortcuts import render, redirect
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
# Create your views here.
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from messaging.models import Message
from django.db.models import Prefetch

User = get_user_model()

@login_required
def delete_user(request):
    if request.method == 'POST':
        user = request.user
        user.delete()
        messages.success(request, "Your account and related data have been deleted.")
        return redirect('login')  # or homepage


def get_user_threads(user):
    # Top-level messages (not replies)
    top_level_messages = Message.objects.filter(
        receiver=user,
        parent_message__isnull=True
    ).select_related('sender').prefetch_related(
        Prefetch('replies', queryset=Message.objects.select_related('sender'))
    )
    return top_level_messages

def get_thread(message):
    """Recursively retrieve all replies in a threaded format"""
    thread = {
        'message': message,
        'replies': [get_thread(reply) for reply in message.replies.all()]
    }
    return thread

def inbox_view(request):
    user = request.user
    unread_messages = Message.unread.for_user(user)
    
# Function-based view
@cache_page(60)  # 60 seconds
def message_list(request):
    messages = Message.objects.all()
    return render(request, 'messaging/message_list.html', {'messages': messages})    

