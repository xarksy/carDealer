from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import  viewsets, filters, permissions, status
from rest_framework.response import Response
from ..models import Cars
from .serializers import CarsSerializer
from django_filters.rest_framework import DjangoFilterBackend
from carShowRoom.api.permissions import IsAdminOrSuperuser, IsStaffOrReadOnly
from rest_framework.decorators import action
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

@method_decorator(cache_page(60 * 5), name='list') # cache for 5 minutes
class CarsViewSet(viewsets.ModelViewSet):
    queryset = Cars.objects.all().order_by('id')
    serializer_class = CarsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['merek', 'model', 'tahun', 'jenis_bahan_bakar']
    search_fields = ['nama','merek']
    ordering_fields = ['harga', 'tahun']
    permission_classes = [IsAdminOrSuperuser]

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def available(self, request):
        cars = Cars.objects.filter(status='available')
        serializer = self.get_serializer(cars, many=True)
        return Response(serializer.data)

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