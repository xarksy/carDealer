from rest_framework import viewsets, permissions, status, filters
from rest_framework.response import Response
from ..models import Order
from .serializers import OrderSerializer, TradeInCarSerializer
from customer.models import Customer
from cars.models import Cars
from carShowRoom.api.permissions import IsAdminOrSuperuser
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related("customer", "showroom_car", "trade_in_car")
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['payment_method', 'status', 'created_by__username']
    search_fields = ['customer__name']
    ordering_fields = ['created_at', 'total']
    ordering = ['-created_at']
    
    def get_queryset(self):
        """
        Filter orders based on user role:
        - Admins & superusers: all orders
        - Sales: all orders (read-only)
        - Customers: only their own orders
        """
        user = self.request.user

        # 🧩 Admin / superuser → all orders
        if user.is_superuser or getattr(user, "role", "") == "admin":
            return Order.objects.all().select_related("customer","showroom_car","trade_in_car")

        # 🧩 Salesperson → all orders, but can’t modify
        if user.is_staff or getattr(user, "role", "") == "sales":
            return Order.objects.all().select_related("customer", "showroom_car","trade_in_car")
        
        # 🧩 Customer → only own orders
        if getattr(user, "role", "") == "customer":
            return Order.objects.filter(customer__user=user).select_related("customer", "showroom_car", "trade_in_car")
        
        # default fallback
        return Order.objects.none()

    def get_permissions(self):
        user = self.request.user

        if not user.is_authenticated:
            return [permissions.IsAuthenticated()] # must log in
        
        # 🧩 Admin: full access
        if user.is_superuser or getattr(user, "role", "") == "admin":
            return [IsAdminOrSuperuser()]

        # 🧩 Salesperson: can only read orders (no create/delete)
        if user.is_staff or getattr(user, "role", "") == "sales":
            return [permissions.IsAuthenticatedOrReadOnly()]
        
        # 🧩 Customer: can create (buy/sell/trade-in), view own orders only
        if getattr(user, "role", "") == "customer":
            return [permissions.IsAuthenticated()]

        return [permissions.IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        customer_id = request.data.get("customer_id")
        showroom_car_id = request.data.get("showroom_car_id")
        offer_type = request.data.get("offer_type")
        trade_in_car_data = request.data.get("trade_in_car")

        if not customer_id or not offer_type:
            return Response({"error": "customer_id and offer_type are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            customer = Customer.objects.get(id=customer_id)
        except Customer.DoesNotExist:
            return Response({"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND)

        showroom_car = None
        if showroom_car_id:
            try:
                showroom_car = Cars.objects.get(id=showroom_car_id)
            except Cars.DoesNotExist:
                return Response({"error": "Showroom car not found"}, status=status.HTTP_404_NOT_FOUND)
        
        trade_in_car = None
        if trade_in_car_data:
            trade_in_car_serializer = TradeInCarSerializer(data=trade_in_car_data)
            if trade_in_car_serializer.is_valid():
                trade_in_car = trade_in_car_serializer.save(customer=customer)
            else:
                return Response(trade_in_car_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        order = Order.objects.create(
            customer=customer,
            showroom_car=showroom_car,
            offer_type=offer_type,
            trade_in_car=trade_in_car,
        )

        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(detail=False, methods=['get'])
    def summary(self, request):
        total = self.get_queryset().count()
        return Response({"total_orders:": total})