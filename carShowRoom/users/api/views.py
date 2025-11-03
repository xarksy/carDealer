from users.api.serializers import UserSerializer
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from carShowRoom.api.permissions import IsAdminOrSuperuser, IsStaffOrReadOnly
from rest_framework import  viewsets, filters, permissions, status
from ..models import User


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrSuperuser]