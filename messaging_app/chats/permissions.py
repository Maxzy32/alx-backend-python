from rest_framework import permissions

class IsParticipantOfConversation(permissions.BasePermission):
    """
    Custom permission to allow only participants of a conversation to view or modify it.
    """

    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        # Covers GET, PUT, PATCH, DELETE – requires user to be a participant
        if request.method in ['GET', 'PUT', 'PATCH', 'DELETE']:
            return request.user in obj.conversation.participants.all()
        return True
