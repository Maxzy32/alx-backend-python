# messaging/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.contrib.auth import logout
from django.contrib.auth.models import User
from messaging_app.chats.serializers import MessageSerializer 

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Message
from messaging_app.chats.serializers import MessageSerializer

from rest_framework.permissions import IsAuthenticated

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

class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Message.objects.select_related('sender', 'receiver', 'parent_message') \
                              .prefetch_related('replies') \
                              .filter(receiver=self.request.user)

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

def get_threaded_replies(request, message_id):
    """Returns a message and all its replies recursively"""
    message = get_object_or_404(Message, id=message_id)

    def fetch_replies(msg):
        replies = []
        for r in msg.replies.all():
            replies.append(r)
            replies += fetch_replies(r)
        return replies

    replies = fetch_replies(message)
    serialized = MessageSerializer([message] + replies, many=True)
    return Response(serialized.data)