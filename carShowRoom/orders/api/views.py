from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from models import Order, TradeInCar
from serializers import OrderSerializer, TradeInCarSerializer
from customer.models import Customer
from cars.models import Cars

class IsAdminOrSalesCanView(permissions.BasePermission):
    """
    Allow GET requests only for users with admin or sales roles.
    Other users can still create orders (POST).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            user = request.user
            # adjust based on your user model
            return user.is_authenticated and (user.is_superuser or getattr(user, "role", "") in ["admin", "sales"])
        return True  # Allow POST/PUT/DELETE for authenticated users

