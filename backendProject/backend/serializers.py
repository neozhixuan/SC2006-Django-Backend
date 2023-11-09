from rest_framework import serializers
from .models import *


class OrderDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderData
        fields = '__all__'


class SuggestionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suggestions
        fields = '__all__'


class PredictionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Predictions
        fields = '__all__'


class SupplierSerializer(serializers.ModelSerializer):
    class Meta:
        model = Supplier
        fields = '__all__'


class ItemNameSerializer(serializers.Serializer):
    label = serializers.CharField()
    value = serializers.CharField()

# To serialize a list
# class ItemNameSerializer(serializers.Serializer):
#     item_names = serializers.ListField(child=serializers.CharField())
