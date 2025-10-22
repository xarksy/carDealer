from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import  viewsets, filters, permissions, status
from rest_framework.response import Response
from ..models import Cars
from .serializers import CarsSerializer
from carShowRoom.api.permissions import IsAdminOrSuperuser, IsStaffOrReadOnly


class CarsViewSet(viewsets.ModelViewSet):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nama','merek']
    ordering_fields = ['harga', 'tahun']
    permission_classes = [IsAdminOrSuperuser]

    def get_permissions(self):
        user = self.request.user

        if not user.is_authenticated:
            return [permissions.AllowAny()]  # public can’t modify, only view if needed

        # 🧩 Admin / Superuser: full access
        if user.is_superuser or getattr(user, "role", "") == "admin":
            return [IsAdminOrSuperuser()]
        
        # 🧩 Salesperson (staff): read and update only
        if user.is_staff or getattr(user, "role", "") == "sales":
            return [IsStaffOrReadOnly()]
        
        # 🧩 Customer: read-only
        if getattr(user, "role", "") == "customer":
            return [permissions.IsAuthenticatedOrReadOnly()]

        # Default fallback
        return [permissions.IsAuthenticated()]