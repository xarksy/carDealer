from rest_framework.permissions import BasePermission

class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if not user or not user.is_authenticated:
            return False
        return user.is_superuser or getattr(user, "role", "") == "admin"

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET','HEAD']:
            return True
        return request.user.is_staff

