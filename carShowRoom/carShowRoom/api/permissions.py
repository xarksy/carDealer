from rest_framework.permissions import BasePermission

class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.is_superuser or getattr(user, "role", "") == "admin"

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET', 'HEAD', 'OPTIONS']:
            return True
        return request.user and request.user.is_authenticated and request.user.is_staff


class IsCustomerReadOnly(BasePermission):
    """Customers can only read (GET), not modify."""
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        # Allow read-only for customers
        if getattr(user, "role", "") == "customer" and request.method in BasePermission.SAFE_METHODS:
            return True
        # Block modifications
        return False
