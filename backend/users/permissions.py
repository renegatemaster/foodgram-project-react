from rest_framework.permissions import BasePermission

GUEST_METHODS = ('GET', 'POST', 'OPTIONS', 'HEAD')


class UserPermission(BasePermission):
    """Allows guests to list, retrieve and post users."""

    def has_permission(self, request, view):
        return True

    def has_object_permission(self, request, view, obj):
        if request.method in GUEST_METHODS:
            return True
        return obj == request.user or request.user.is_superuser
