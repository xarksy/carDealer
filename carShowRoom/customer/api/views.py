from rest_framework import viewsets, status, filters
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend
from models import Customer
from .serializers import CustomerSerializer, CustomerDetailSerializer

class CustomerViewSet(viewsets.ModelViewSet):
    queryset = Customer.objects.all().order_by('-created_at')
    serializer_class = CustomerSerializer
    permission_classes = [IsAuthenticated]

    # 🔍 Enable search & filtering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['status']  # example: ?status=deal
    search_fields = ['name', 'phone_number', 'email']  # example: ?search=john
    ordering_fields = ['created_at', 'updated_at', 'name']
    ordering = ['-created_at']

    