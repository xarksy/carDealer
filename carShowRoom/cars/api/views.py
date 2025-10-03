from rest_framework.permissions import IsAuthenticated
from rest_framework import  viewsets
from ..models import Cars
from .serializers import CarsSerializer
from .permissions import IsAdminOrSuperuser


class CarsViewSet(viewsets.ModelViewSet):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer
    permission_classes = [IsAdminOrSuperuser]