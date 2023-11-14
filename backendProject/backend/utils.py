# backendProject/backend/utils.py
from .models import *
from .serializers import *
from .models import *

from django.db import transaction
import firebase_admin
from firebase_admin import credentials, firestore, initialize_app

import sys
import requests


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