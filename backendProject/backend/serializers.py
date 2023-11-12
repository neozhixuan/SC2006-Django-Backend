from rest_framework import serializers
from .models import *


class OrderDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderData
        fields = '__all__'


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = '__all__'


class MarketplaceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Marketplace
        fields = '__all__'


class PredictionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predictions
        fields = '__all__'


class SuggestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestions
        fields = '__all__'


class SuppliersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suppliers
        fields = '__all__'


class ItemNameSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.CharField()
