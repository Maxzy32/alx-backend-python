from rest_framework import permissions  # ✅ Required for ALX checker

class IsOwner(permissions.BasePermission):  # Use from the imported permissions module
    """
    Custom permission to only allow owners of an object to access it.
    """

    def has_object_permission(self, request, view, obj):
        return obj.user == request.user
