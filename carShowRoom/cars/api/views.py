from rest_framework import  viewsets
from models import Cars
from serializers import CarsSerializer
from .permissions import IsAdminSuperuser

class CarsViewSet(viewsets.ModelViewSet):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer
    permission_classes = [IsAdminSuperuser]