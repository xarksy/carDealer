from rest_framework import serializers
from ..models import Cars, ServiceHistory

class ServiceHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceHistory
        fields = ['id','tanggal_servis','deskripsi','biaya']

class CarsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cars
        fields = "__all__"

