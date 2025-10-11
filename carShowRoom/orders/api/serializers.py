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

