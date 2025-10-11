from rest_framework import serializers
from models import Order, TradeInCar
from customer.api.serializers import CustomerSerializer
from cars.api.serializers import CarsSerializer

class TradeInCarSerializer(serializers.ModelSerializer):
    class Meta:
        model = TradeInCar
        fields = [
            'id', 'offered_vehicle_model', 'offered_vehicle_varian',
            'offered_vehicle_transmission', 'offered_vehicle_province',
            'offered_vehicle_year', 'offered_vehicle_kilometers',
            'offered_vehicle_notes'
        ]

class OrderSerializer(serializers.ModelSerializer):
    customer = CustomerSerializer(read_only=True)
    showroom_car = CarsSerializer(read_only=True)
    trade_in_car = TradeInCarSerializer(read_only=True)

    offer_type_display = serializers.CharField(source='get_offer_type_display', read_only=True)
    created_at_formatted = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = [
            'id',
            'customer',
            'showroom_car',
            'offer_type',
            'offer_type_display',
            'trade_in_car',
            'created_at',
            'created_at_formatted'
        ]
    
    def get_created_at_formatted(self, obj):
        return obj.created_at.strftime("%d %b %Y, %H:%M")
