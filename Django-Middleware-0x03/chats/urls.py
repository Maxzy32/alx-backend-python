# chats/urls.py
from django.urls import path, include
from rest_framework import routers  # ✅ ALX requires this import explicitly
from rest_framework_nested.routers import NestedDefaultRouter
# from .views import ConversationViewSet, MessageViewSet
from chats.views import ConversationViewSet, MessageViewSet



router = routers.DefaultRouter()
router.register(r'conversations', ConversationViewSet, basename='conversations')

# Nested router for messages under each conversation
conversation_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversation_router.urls)),
]
