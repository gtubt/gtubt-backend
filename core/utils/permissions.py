from rest_framework.permissions import BasePermission

SAFE_METHODS = ["GET"]


class IsAdminOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if (
            request.method not in SAFE_METHODS
            and request.user
            and request.user.is_authenticated
            and request.user.is_superuser
        ):
            return True
        elif request.method in SAFE_METHODS:
            return True

        return False
