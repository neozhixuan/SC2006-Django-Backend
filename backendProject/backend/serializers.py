from rest_framework import serializers
from .models import OrderData


class OrderDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderData
        fields = '__all__'
