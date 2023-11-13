from datetime import datetime, timedelta
from .serializers import *
from .models import *

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics

import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render

import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')

##########################
# Firebase Connection to Django REST API
##########################
script_path = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(script_path, "credentials.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
db = firestore.Client()
try:
    firebase_admin
except NameError:
    cred = credentials.Certificate(credentials_path)
    firebase_admin = initialize_app(cred)
##########################

##########################
# Update our Models.py upon runserver
##########################


def update_model_from_firestore(model_class, document_name):
    db = firestore.Client()
    doc_ref = db.collection('Database').document(document_name)
    document_data = doc_ref.get().to_dict()

    # Use transaction to ensure atomicity of updates
    with transaction.atomic():
        # Iterate through each field in the document and update the model
        for item_name, item_data in document_data.items():
            # Check if the item already exists in the model
            model_item, created = model_class.objects.get_or_create(
                item_name=item_name)

            # Update the fields based on Firestore data
            for field_name, field_value in item_data.items():
                print(f"Field: {field_name}, Value: {field_value}")
                setattr(model_item, field_name.lower(), field_value)

            # Save the changes
            model_item.save()
##########################


##########################
# API Endpoints
##########################
@api_view(['GET'])
def index(request):
    return HttpResponse("Hello, world. You're at the sc2006 backend.")


@api_view(['GET'])
def filterForExpiringStock(request):
    # Perform filtering on the Inventory for low stock
    now = datetime.now()
    two_days_from_now = now + timedelta(days=2)
    filtered_data = Inventory.objects.filter(ExpiryDate__lte=two_days_from_now)
    serializer = InventorySerializer(filtered_data, many=True)
    return Response(serializer.data)


@api_view(['GET'])
def getItemNames(request):
    # Get a list of item names
    itemNames = Inventory.objects.values_list('ItemName', flat=True)
    formattedNames = [{"label": itemName, "value": itemName}
                      for itemName in itemNames]
    serializer = ItemNameSerializer(formattedNames, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def createInventory(request):
    serializer = InventorySerializer(data=request.data)

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
    serializer = SuppliersSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

##########################
# REST API List Display
#########################


class InventoryList(generics.ListCreateAPIView):
    queryset = Inventory.objects.all()  # Add this line
    serializer_class = InventorySerializer

    def get(self, request, *args, **kwargs):
        # Call the function to update the 'Inventory' model
        update_model_from_firestore(Inventory, 'Inventory')

        # Continue with the original get method logic if needed
        return super().get(request, *args, **kwargs)


class MarketplaceList(generics.ListCreateAPIView):
    queryset = Marketplace.objects.all()
    serializer_class = MarketplaceSerializer

    def get(self, request, *args, **kwargs):
        # Call the function to update the 'Marketplace' model
        update_model_from_firestore(Marketplace, "Marketplace")

        # Continue with the original get method logic if needed
        return super().get(request, *args, **kwargs)


class SupplierList(generics.ListCreateAPIView):
    queryset = Suppliers.objects.all()
    serializer_class = SuppliersSerializer

    def get(self, request, *args, **kwargs):
        # Call the function to update the 'Suppliers' model
        update_model_from_firestore(Suppliers, "Suppliers")

        # Continue with the original get method logic if needed
        return super().get(request, *args, **kwargs)


class SuggestionsList(generics.ListCreateAPIView):
    queryset = Suggestions.objects.all()
    serializer_class = SuggestionsSerializer


class SuggestionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Suggestions.objects.all()
    serializer_class = SuggestionsSerializer


class PredictionsList(generics.ListCreateAPIView):
    queryset = Predictions.objects.all()
    serializer_class = PredictionsSerializer


class PredictionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Predictions.objects.all()
    serializer_class = PredictionsSerializer

##########################
