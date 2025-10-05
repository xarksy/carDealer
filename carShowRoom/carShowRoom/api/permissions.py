from rest_framework.permissions import BasePermission

class IsAdminOrSuperuser(BasePermission):
    def has_permission(self, request, view):
        user = request.user
        return bool (
            user
            and user.is_authenticated
            and (user.is_authenticated or getattr(user, "role", None) == "admin")
        )

class IsStaffOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in ['GET','HEAD']:
            return True
        return request.user.is_staff

