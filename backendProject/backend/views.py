import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from django.shortcuts import render
from django.http import HttpResponse
import firebase_admin
from firebase_admin import credentials, firestore


from rest_framework import generics
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import *
from .serializers import *

from datetime import datetime, timedelta

## Firebase Connection
import os
from firebase_admin import credentials, initialize_app
from google.cloud import firestore
script_path = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(script_path, "credentials.json")
# Environment Variable so that Django can detect your account details
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path
cred = credentials.Certificate(credentials_path)
firebase_admin = initialize_app(cred)

# Initialize Firestore client
db = firestore.Client()

def view_firestore_data(request):
    
    # Specify the collection, document, and field you want to retrieve
    col_Inventory = 'Inventory'
    Inventory_doc = 'Ingredient_Bun'
    Inventory_field = 'Bun'

    # Query Firestore
    doc_ref = db.collection(col_Inventory).document(Inventory_doc)
    document_data = doc_ref.get()

    # Extract the value of the specified field
    map_field = document_data.get(Inventory_field) if document_data.exists else None

    # Pass the data to the template
    context = {
        'Inventory': col_Inventory,
        'Ingredient_Bun': Inventory_doc,
        'Inventory_field': Inventory_field,
        'map_field': map_field,
    }
 
    return render(request, '../templates/index.html', context)
    

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


class SupplierList(generics.ListCreateAPIView):
    queryset = Supplier.objects.all()
    serializer_class = SupplierSerializer
