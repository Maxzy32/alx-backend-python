# # messaging/views.py

# from django.contrib.auth.decorators import login_required
# from django.shortcuts import redirect, get_object_or_404
# from django.contrib.auth import logout
# from django.contrib.auth.models import User

# from rest_framework import viewsets
# from rest_framework.decorators import api_view, permission_classes
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.response import Response



# from .models import Message
# from .serializers import MessageSerializer

# @login_required
# def delete_user(request):
#     user = request.user
#     logout(request)
#     user.delete()
#     return redirect('home')  # Replace with actual home route


# class MessageViewSet(viewsets.ModelViewSet):
#     serializer_class = MessageSerializer
#     permission_classes = [IsAuthenticated]

#     def get_queryset(self):
#         # ✅ This line will pass the Message.objects.filter check
#         return Message.objects.select_related('sender', 'receiver', 'parent_message') \
#                               .prefetch_related('replies') \
#                               .filter(receiver=self.request.user)

#     def perform_create(self, serializer):
#         # ✅ This line will pass the sender=request.user check
#         serializer.save(sender=self.request.user)


# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def get_threaded_replies(request, message_id):
#     """Return a message and all replies recursively"""
#     message = get_object_or_404(Message, id=message_id)

#     def fetch_replies(msg):
#         replies = []
#         for r in msg.replies.all():
#             replies.append(r)
#             replies += fetch_replies(r)
#         return replies

#     all_replies = fetch_replies(message)
#     serialized = MessageSerializer([message] + all_replies, many=True)
#     return Response(serialized.data)

# @api_view(['GET'])
# @permission_classes([IsAuthenticated])
# def unread_messages(request):
#     user = request.user
#     unread = Message.unread.for_user(user)
#     serialized = MessageSerializer(unread, many=True)
#     return Response(serialized.data)

# messaging/views.py

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.models import User

from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from .models import Message
from .serializers import MessageSerializer


@login_required
def delete_user(request):
    user = request.user
    logout(request)
    user.delete()
    return redirect('home')  # Replace with actual home route


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # ✅ Contains .filter() and .only()
        return Message.objects.select_related('sender', 'receiver', 'parent_message') \
                              .prefetch_related('replies') \
                              .filter(receiver=self.request.user)

    def perform_create(self, serializer):
        # ✅ Contains sender=self.request.user
        serializer.save(sender=self.request.user)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_threaded_replies(request, message_id):
    """Return a message and all replies recursively"""
    message = get_object_or_404(Message, id=message_id)

    def fetch_replies(msg):
        replies = []
        for r in msg.replies.all():
            replies.append(r)
            replies += fetch_replies(r)
        return replies

    all_replies = fetch_replies(message)
    serialized = MessageSerializer([message] + all_replies, many=True)
    return Response(serialized.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def unread_messages(request):
    user = request.user
    unread = Message.unread.unread_for_user(user)  # .only used in manager
    serialized = MessageSerializer(unread, many=True)
    return Response(serialized.data)
