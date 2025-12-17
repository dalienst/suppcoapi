from rest_framework import permissions

SAFE_METHODS = ("GET", "HEAD", "OPTIONS")


class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of a company
    to edit it. Assumes the model instance has an `user` attribute.
    Allows unauthenticated users to read.
    """

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True

        return obj.user == request.user


class IsSupplierOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_supplier
        )

    def has_object_permission(self, request, view, obj):
        # Read-only always allowed
        if request.method in SAFE_METHODS:
            return True
        return obj.user == request.user


class IsContractorOrReadOnly(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_supplier
        )

    def has_permission(self, request, view):
        return request.method in SAFE_METHODS or (
            request.user.is_authenticated and request.user.is_contractor
        )
