# messaging/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User

from .models import Message

@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Logs the user out first
    user.delete()
    return redirect('home')  # Replace with your actual home route or URL

def get_conversation_queryset():
    return (
        Message.objects
        .select_related('sender', 'receiver', 'parent_message')
        .prefetch_related('replies')
        .all()
    )
