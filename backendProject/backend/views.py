from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import *
from .serializers import *

from datetime import datetime, timedelta


@api_view(['GET'])
def index(request):
    return HttpResponse("Hello, world. You're at the sc2006 backend.")


@api_view(['GET'])
def filterForExpiringStock(request):
    # Perform filtering on the OrderData for low stock
    now = datetime.now()
    two_days_from_now = now + timedelta(days=2)
    filtered_data = OrderData.objects.filter(ExpiryDate__lte=two_days_from_now)
    serializer = OrderDataSerializer(filtered_data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getItemNames(request):
    # Get a list of item names
    itemNames = OrderData.objects.values_list('ItemName', flat=True)
    formattedNames = [{"label": itemName, "value": itemName}
                      for itemName in itemNames]
    serializer = ItemNameSerializer(formattedNames, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def createOrderData(request):
    serializer = OrderDataSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def createSuggestion(request):
    serializer = SuggestionsSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def createPrediction(request):
    serializer = PredictionsSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def createSupplier(request):
    serializer = SupplierSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

##########################
# REST API List Display
#########################


class OrderDataList(generics.ListCreateAPIView):
    queryset = OrderData.objects.all()
    serializer_class = OrderDataSerializer


class OrderDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderData.objects.all()
    serializer_class = OrderDataSerializer


class SuggestionsList(generics.ListCreateAPIView):
    queryset = Suggestions.objects.all()
    serializer_class = OrderDataSerializer


class SuggestionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Suggestions.objects.all()
    serializer_class = OrderDataSerializer


class PredictionsList(generics.ListCreateAPIView):
    queryset = Predictions.objects.all()
    serializer_class = OrderDataSerializer


class PredictionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Predictions.objects.all()
    serializer_class = OrderDataSerializer


class SupplierList(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = OrderDataSerializer
