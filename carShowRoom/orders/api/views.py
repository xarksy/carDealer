from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from models import Order, TradeInCar
from serializers import OrderSerializer, TradeInCarSerializer
from customer.models import Customer
from cars.models import Cars

class IsAdminOrSalesCanView(permissions.BasePermission):
    """
    Allow GET requests only for users with admin or sales roles.
    Other users can still create orders (POST).
    """
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            user = request.user
            # adjust based on your user model
            return user.is_authenticated and (user.is_superuser or getattr(user, "role", "") in ["admin", "sales"])
        return True  # Allow POST/PUT/DELETE for authenticated users

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all().select_related("customer", "showroom_car", "trade_in_car")
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminOrSalesCanView]

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
