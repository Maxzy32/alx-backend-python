from django.shortcuts import get_object_or_404
from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_403_FORBIDDEN
from rest_framework.exceptions import PermissionDenied

from .models import Conversation, Message, User
from .serializers import ConversationSerializer, MessageSerializer
from .permissions import IsParticipantOfConversation
from .filters import MessageFilter
from .pagination import StandardResultsSetPagination
from django_filters.rest_framework import DjangoFilterBackend
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

# class ConversationViewSet(viewsets.ModelViewSet):
#     queryset = Conversation.objects.all()
#     serializer_class = ConversationSerializer
#     permission_classes = [IsParticipantOfConversation]
#     filter_backends = [filters.OrderingFilter]
#     ordering_fields = ['created_at']

#     def get_queryset(self):
#         return Conversation.objects.filter(participants=self.request.user)

#     def perform_create(self, serializer):
#         conversation = serializer.save()
#         conversation.participants.add(self.request.user)


# class MessageViewSet(viewsets.ModelViewSet):
#     serializer_class = MessageSerializer
#     permission_classes = [IsParticipantOfConversation]
#     filter_backends = [DjangoFilterBackend, filters.OrderingFilter]  # ✅ Fix indentation here
#     filterset_class = MessageFilter
#     pagination_class = StandardResultsSetPagination
#     ordering_fields = ['sent_at']

#     def get_queryset(self):
#         conversation_id = self.kwargs.get('conversation_pk')
#         conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

#         if not self.request.user.is_authenticated:
#             raise PermissionDenied("Authentication required")

#         if not conversation.participants.filter(user_id=self.request.user.user_id).exists():
#             raise PermissionDenied(detail="You are not a participant in this conversation.", code=HTTP_403_FORBIDDEN)

#         return Message.objects.filter(conversation=conversation)

#     def perform_create(self, serializer):
#         conversation_id = self.kwargs.get('conversation_pk')
#         conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

#         if not self.request.user.is_authenticated:
#             raise PermissionDenied("Authentication required")

#         if not conversation.participants.filter(user_id=self.request.user.user_id).exists():
#             raise PermissionDenied(detail="You are not a participant in this conversation.", code=HTTP_403_FORBIDDEN)

#         serializer.save(sender=self.request.user, conversation=conversation)

@method_decorator(cache_page(60), name='list')
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsParticipantOfConversation]
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_class = MessageFilter
    pagination_class = StandardResultsSetPagination
    ordering_fields = ['sent_at']

    def get_queryset(self):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

        if not self.request.user.is_authenticated:
            raise PermissionDenied("Authentication required")

        if not conversation.participants.filter(user_id=self.request.user.user_id).exists():
            raise PermissionDenied(detail="You are not a participant in this conversation.", code=HTTP_403_FORBIDDEN)

        return Message.objects.filter(conversation=conversation)

    def perform_create(self, serializer):
        conversation_id = self.kwargs.get('conversation_pk')
        conversation = get_object_or_404(Conversation, conversation_id=conversation_id)

        if not self.request.user.is_authenticated:
            raise PermissionDenied("Authentication required")

        if not conversation.participants.filter(user_id=self.request.user.user_id).exists():
            raise PermissionDenied(detail="You are not a participant in this conversation.", code=HTTP_403_FORBIDDEN)

        serializer.save(sender=self.request.user, conversation=conversation)
