from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import  viewsets, filters, permissions, status
from rest_framework.response import Response
from ..models import Cars
from .serializers import CarsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from carShowRoom.api.permissions import IsAdminOrSuperuser, IsStaffOrReadOnly


class CarsViewSet(viewsets.ModelViewSet):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['merek', 'model', 'tahun', 'jenis_bahan_bakar']
    search_fields = ['nama','merek']
    ordering_fields = ['harga', 'tahun']
    permission_classes = [IsAdminOrSuperuser]

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({
            "message": "Car successfully added",
            "data": response.data
        }, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        """Handle both PUT and PATCH for updating cars."""
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(
            {"message": "Car successfully updated", "data": serializer.data},
            status=status.HTTP_200_OK
        )
    
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(
            {"message": "Car successfully deleted"},
            status=status.HTTP_204_NO_CONTENT
        )

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