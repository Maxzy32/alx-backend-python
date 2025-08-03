# messaging/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User

@login_required
def delete_user(request):
    user = request.user
    logout(request)  # Logs the user out first
    user.delete()
    return redirect('home')  # Replace with your actual home route or URL
