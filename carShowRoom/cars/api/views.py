from rest_framework import  viewsets
from models import Cars
from serializers import CarsSerializer

class CarsViewSet(viewsets.ModelViewSet):
    queryset = Cars.objects.all()
    serializer_class = CarsSerializer