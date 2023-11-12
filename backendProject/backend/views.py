import sys
import os

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
from django.shortcuts import render
from django.http import HttpResponse
from django.db import transaction
from django.db.models import DateTimeField
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
#from google.cloud import firestore

# Determine the path to the credentials file
script_path = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(script_path, "credentials.json")

# Environment Variable so that Django can detect your account details
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Initialize Firestore client
db = firestore.Client()

# Initialize Firebase app (ensure it's done only once)
try:
    firebase_admin
except NameError:
    cred = credentials.Certificate(credentials_path)
    firebase_admin = initialize_app(cred)


def update_model_from_firestore(model_class, document_name):
    # Initialize Firestore client
    db = firestore.Client()


    # Specify the document you want to retrieve under the "Database" collection
    doc_ref = db.collection('Database').document(document_name)
    document_data = doc_ref.get().to_dict()
    
    #debug print
    print(document_data)

    # Use transaction to ensure atomicity of updates
    with transaction.atomic():
        # Iterate through each field in the document and update the model
        for item_name, item_data in document_data.items():
            #debug print
            print(f"Processing item: {item_name}")
            # Check if the item already exists in the model
            model_item, created = model_class.objects.get_or_create(item_name=item_name)
            
            # Update the fields based on Firestore data
            # Adjust this part based on your actual field names in the model
            for field_name, field_value in item_data.items():
                print(f"Field: {field_name}, Value: {field_value}")
                setattr(model_item, field_name.lower(), field_value)

            # Save the changes
            model_item.save()

# Call the function to update the 'Inventory' model
update_model_from_firestore(Inventory, 'Inventory')
# Call the function to update the 'Marketplace' model
update_model_from_firestore(Marketplace, 'Marketplace')

# def map_firestore_data_to_models(data):
#     models_mapping = {
#         'Inventory': Inventory,
#         'Marketplace': Marketplace,
#         'Prediction': Predictions,
#         'Suggestions': Suggestions,
#         'Suppliers': Supplier,
#     }

#     mapped_data = {}

#     for document, model_class in models_mapping.items():
#         document_data = data.get(document, {})
        
# # Iterate through each field in the document
#         for item_name, item_data in document_data.items():
#             # Create an instance of the model for each item
#             model_instance = model_class.objects.create(
#                 **item_data  # Use all other fields from the Firestore data
#             )
            
#             # Save the created instance in the mapped data
#             mapped_data.setdefault(document, []).append(model_instance)

#     return mapped_data

# def view_firestore_data(request):
    
    
#     # Specify the documents you want to retrieve under the "Database" collection
#     documents = ['Inventory', 'Marketplace', 'Prediction', 'Suggestions', 'Suppliers']

#     # Query Firestore for each document
#     data = {}
#     for document in documents:
#         doc_ref = db.collection('Database').document(document)
#         document_data = doc_ref.get()

#         # Extract the data from the document
#         data[document] = document_data.to_dict() if document_data.exists else None

#     # Map Firestore data to Django models
#     mapped_data = map_firestore_data_to_models(data)

#     inventory_instance = Inventory.objects.all()
#     # Pass the mapped data to the template
#     context = {
#         'mapped_data': mapped_data,
#         'inventory_instance': Inventory.objects.all(),  # Example for accessing Inventory
#     }
 
#     return render(request, '../templates/index.html', context)

    

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


# @api_view(['POST'])
# def createSupplier(request):
#     serializer = SuppliersSerializer(data=request.data)

#     if serializer.is_valid():
#         serializer.save()
#         return Response(serializer.data, status=status.HTTP_201_CREATED)
#     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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
        update_model_from_firestore(Marketplace, "Marketplace")

        # Continue with the original get method logic if needed
        return super().get(request, *args, **kwargs)
    
# class SuppliersList(generics.ListCreateAPIView):
#     queryset = Suppliers.objects.all()
#     serializer_class = SuppliersSerializer
#     def get(self, request, *args, **kwargs):
#         update_model_from_firestore(Suppliers, "Suppliers")

#         # Continue with the original get method logic if needed
#         return super().get(request, *args, **kwargs)

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
