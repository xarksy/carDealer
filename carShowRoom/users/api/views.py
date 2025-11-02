from rest_framework.views import APIView
from rest_framework.response import Response
from users.api.serializers import UserSerializer
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from carShowRoom.api.permissions import IsAdminOrSuperuser, IsStaffOrReadOnly


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data)