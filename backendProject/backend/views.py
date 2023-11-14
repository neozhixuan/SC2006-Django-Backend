import firebase_admin
from firebase_admin import firestore, credentials, initialize_app

import os
import sys

from datetime import datetime, timedelta
from .serializers import *
from .models import *

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import generics
from rest_framework import status

from django.db import transaction
from django.http import HttpResponse
from django.shortcuts import render


import requests

sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
# Set up Firebase credentials
script_path = os.path.dirname(os.path.abspath(__file__))
credentials_path = os.path.join(script_path, "credentials.json")
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

# Initialize Firebase Admin SDK
try:
    firebase_admin
except NameError:
    cred = credentials.Certificate(credentials_path)
    firebase_admin = initialize_app(cred)

# Initialize Firestore client
db = firestore.Client()


def update_model_from_firestore(model_class, document_name):
    db = firestore.Client()
    doc_ref = db.collection('Database').document(document_name)
    document_data = doc_ref.get().to_dict()

    # Use transaction to ensure atomicity of updates
    with transaction.atomic():
        # Iterate through each field in the document and create a new model entry
        for item_name, item_data in document_data.items():

            # Create a new entry for each item_id
            model_instance = model_class.objects.create(item_name=item_name, **item_data)


##########################
# Suggestions Logic
##########################


def get_weather_data():
    # Use the data.gov.sg weather API endpoint or your specific API endpoint
    api_url = "https://api.data.gov.sg/v1/environment/24-hour-weather-forecast"

    # Make a request to the API
    response = requests.get(api_url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        weather_data = response.json()
        return weather_data
    else:
        # Handle the case where the request was not successful
        print(f"Error: {response.status_code}")
        return None


def check_ingredient_availability(ingredients, required_ingredients):
    for ingredient_name, required_quantity in required_ingredients.items():
        ingredient_found = False
        for ingredient in ingredients:
            if (
                ingredient["ingredient_name"] == ingredient_name
                and ingredient["quantity"] >= required_quantity
            ):
                ingredient_found = True
                break  # Exit the inner loop once a match is found
        if not ingredient_found:
            return False  # Exit the outer loop if a required ingredient is not found
    return True  # All required ingredients were found


@api_view(['GET'])
def suggest_menu_items(request):
    menu_items = [
        {"id": 1, "item_name": "Grilled Chicken Sandwich", "ingredients": {
            "Chicken Breast": 1, "Mixed Greens": 1, "Tomatoes": 1}},
        {"id": 2, "item_name": "Vegetarian Wrap", "ingredients": {
            "Pasta": 1, "Feta Cheese": 1, "Bell Peppers": 1}},
        {"id": 3, "item_name": "Tomato Basil Pasta", "ingredients": {
            "Pasta": 1, "Tomatoes": 1, "Feta Cheese": 1}},
        {"id": 4, "item_name": "Greek Salad", "ingredients": {
            "Tomatoes": 1, "Feta Cheese": 1, "Mixed Greens": 1}},
        {"id": 5, "item_name": "Mushroom Risotto", "ingredients": {
            "Mushrooms": 1, "Pasta": 1, "Feta Cheese": 1}},
        {"id": 6, "item_name": "Chicken Caesar Salad", "ingredients": {
            "Chicken Breast": 1, "Romaine Lettuce": 1, "Feta Cheese": 1}},
        {"id": 7, "item_name": "Caprese Panini", "ingredients": {
            "Tomatoes": 1, "Feta Cheese": 1, "Chicken Breast": 1}},
        {"id": 8, "item_name": "Vegetable Stir-Fry",
         "ingredients": {"Bell Peppers": 1, "Mushrooms": 1, "Chicken Breast": 1}},
        {"id": 9, "item_name": "Chicken Noodle Soup", "ingredients": {
            "Chicken Breast": 1, "Pasta": 1, "Bell Peppers": 1}},
        {"id": 10, "item_name": "Avocado Toast", "ingredients": {
            "Mixed Greens": 1, "Tomatoes": 1, "Chicken Breast": 1}}
    ]

    ingredients = [
        {"ingredient_name": "Chicken Breast", "quantity": 1},
        {"ingredient_name": "Tomatoes", "quantity": 1},
        {"ingredient_name": "Mixed Greens", "quantity": 1},
        {"ingredient_name": "Mushrooms", "quantity": 1},
        {"ingredient_name": "Pasta", "quantity": 1},
        {"ingredient_name": "Feta Cheese", "quantity": 1},
        {"ingredient_name": "Bell Peppers", "quantity": 1}
    ]
    suggested_menu = []
  # Make sure to call the function with parentheses
    weather_data = get_weather_data()

    # Extract relevant weather information from the API response
    if weather_data and "items" in weather_data:
        # Check if "items" is a list
        if isinstance(weather_data["items"], list) and weather_data["items"]:
            forecast = weather_data["items"][0]["general"]["forecast"].lower()
            humidity_low = weather_data["items"][0]["general"]["relative_humidity"]["low"]
            humidity_high = weather_data["items"][0]["general"]["relative_humidity"]["high"]

            # You can customize this logic based on your menu and the desired weather conditions
            if "thundery showers" in forecast:
                # Suggest warm and hearty dishes for rainy weather and high humidity
                for item in menu_items:

                    if "soup" in item["item_name"].lower() and check_ingredient_availability(ingredients, item.get("ingredients", {})):
                        item["message"] = "Suggested"
                        suggested_menu.append(item)
            elif "partly cloudy" in forecast:
                # Suggest lighter items for partly cloudy weather and low humidity
                for item in menu_items:
                    if "salad" in item["item_name"].lower() and check_ingredient_availability(ingredients, item.get("ingredients", {})):
                        item["message"] = "Suggested"
                        suggested_menu.append(item)
            for item in menu_items:
                if check_ingredient_availability(ingredients, item.get("ingredients", {})):
                    suggested_menu.append(item)

            suggested_menu.append({"forecast": f"{forecast}"})
            suggested_menu.append({"humidity_low": f"{humidity_low}"})
            suggested_menu.append({"humidity_high": f"{humidity_high}"})
        else:
            print(
                "Error: 'items' key is not present or is not a non-empty list in the weather data.")
    else:
        print("Error: Missing 'items' key in the weather data.")

    return Response(suggested_menu)

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
    unique_names_set = set()
    itemNames = Inventory.objects.values_list('item_name', flat=True)
    formattedNames = [{"label": itemName, "value": itemName}
                      for itemName in itemNames if itemName not in unique_names_set and (unique_names_set.add(itemName) or True)]
    serializer = ItemNameSerializer(formattedNames, many=True)

    return Response(serializer.data)


@api_view(['POST'])
def createInventory(request):
    serializer = InventorySerializer(data=request.data)

    if serializer.is_valid():
        # Save the data to the Django model
        instance = serializer.save()

        # Convert the serializer data to a dictionary
        data_dict = serializer.data

        # Initialize Firestore client
        db = firestore.Client()

        # Get a sanitized document ID (replace spaces with underscores)
        document_id = instance.item_name.replace(" ", "_")

        # Get the document reference in Firestore
        doc_ref = db.collection('Database').document('Inventory')

        # Update the data directly under the "Inventory" document
        doc_ref.update({
            document_id: {
                "flow_rate": data_dict["flow_rate"],
                "expiry_date": data_dict["expiry_date"],
                "quantity": data_dict["quantity"],
                "entry_date": data_dict["entry_date"]
            }
        })

        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
def createMarketplace(request):
    serializer = MarketplaceSerializer(data=request.data)

    if serializer.is_valid():
        # Save the data to the Django model
        instance = serializer.save()

        # Convert the serializer data to a dictionary
        data_dict = serializer.data

        # Initialize Firestore client
        db = firestore.Client()

        # Get a sanitized document ID (replace spaces with underscores)
        document_id = instance.item_name.replace(" ", "_")

        # Get the document reference in Firestore
        doc_ref = db.collection('Database').document('Marketplace')

        # Update the data directly under the "Marketplace" document
        doc_ref.update({
            document_id: {
                "expiry_date": data_dict["expiry_date"],
                "price": data_dict["price"],
            }
        })

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
    #update_model_from_firestore(Inventory, 'Inventory')
    # def get(self, request, *args, **kwargs):
    #     # Call the function to update the 'Inventory' model
    #     update_model_from_firestore(Inventory, 'Inventory')

    #     # Continue with the original get method logic if needed
    #     return super().get(request, *args, **kwargs)


class MarketplaceList(generics.ListCreateAPIView):
    queryset = Marketplace.objects.all()
    serializer_class = MarketplaceSerializer
    #update_model_from_firestore(Marketplace, "Marketplace")
    # def get(self, request, *args, **kwargs):
    #     # Call the function to update the 'Marketplace' model
    #     update_model_from_firestore(Marketplace, "Marketplace")

    #     # Continue with the original get method logic if needed
    #     return super().get(request, *args, **kwargs)


class SupplierList(generics.ListCreateAPIView):
    queryset = Suppliers.objects.all()
    serializer_class = SuppliersSerializer

    # def get(self, request, *args, **kwargs):
    #     # Call the function to update the 'Suppliers' model
    #     update_model_from_firestore(Suppliers, "Suppliers")

    #     # Continue with the original get method logic if needed
    #     return super().get(request, *args, **kwargs)


class PredictionsList(generics.ListCreateAPIView):
    queryset = Predictions.objects.all()
    serializer_class = PredictionsSerializer

    # def get(self, request, *args, **kwargs):
    #     # Call the function to update the 'Marketplace' model
    #     update_model_from_firestore(Predictions, "Prediction")

    #     # Continue with the original get method logic if needed
    #     return super().get(request, *args, **kwargs)


class PredictionsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Predictions.objects.all()
    serializer_class = PredictionsSerializer

##########################
