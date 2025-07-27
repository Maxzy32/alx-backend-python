from rest_framework import permissions


class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to view or modify it.
    """

    def has_object_permission(self, request, view, obj):
        # For message-level permissions (obj is a Message)
        return request.user in obj.conversation.participants.all()

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
