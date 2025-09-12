from rest_framework import permissions

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a company
    to edit it. Assumes the model instance has an `user` attribute.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user
