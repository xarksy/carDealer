from rest_framework.permissions import IsAuthenticated
from rest_framework import  viewsets, filters
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
