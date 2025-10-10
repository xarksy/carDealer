from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import  viewsets, filters
from rest_framework.response import Response
from ..models import Cars
from .serializers import CarsSerializer
from carShowRoom.api.permissions import IsAdminOrSuperuser


class CarsViewSet(viewsets.ModelViewSet):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['nama','merek']
    ordering_fields = ['harga', 'tahun']
    permission_classes = [IsAdminOrSuperuser]

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        return Response({"status": "success", "data": response.data})

    def retrieve(self, request, *args, **kwargs):
        response = super().retrieve(request, *args, **kwargs)
        return Response({"status": "success", "data": response.data})

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        return Response({"status": "success", "data": response.data})