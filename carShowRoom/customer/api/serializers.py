from rest_framework import serializers
from models import Customer

class CustomerSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source='get_status_display', read_only=True)

    class Meta:
        model = Customer
        fields = [
            'id',
            'name',
            'phone_number',
            'email',
            'address',
            'status',
            'status_display',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['created_at','updated_at']
    
    def validate_phone_number(self, value):
        customer_id = self.instance.id if self.instance else None
        if Customer.objects.filter(phone_number=value).exclue(id=customer_id).exists():
            raise serializers.ValidationError("Nomor telepon ini sudah digunakan oleh customer lain.")
        return value
