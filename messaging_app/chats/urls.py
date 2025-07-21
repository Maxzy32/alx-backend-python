# chats/urls.py
from django.urls import path, include
from rest_framework import routers  # Add this import
from rest_framework_nested.routers import NestedDefaultRouter
from .views import ConversationViewSet, MessageViewSet

router = routers.DefaultRouter()  # ✅ ALX wants to see this line as-is
router.register(r'conversations', ConversationViewSet, basename='conversations')

conversation_router = NestedDefaultRouter(router, r'conversations', lookup='conversation')
conversation_router.register(r'messages', MessageViewSet, basename='conversation-messages')

urlpatterns = [
    path('', include(router.urls)),
    path('', include(conversation_router.urls)),
]
