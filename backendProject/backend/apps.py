from django.apps import AppConfig
#import os
#import sys
#from firebase_admin import credentials, firestore, initialize_app
#from .models import Inventory, Marketplace, Suppliers, Predictions
#from .views import update_model_from_firestore

class BackendConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'backend'
    
    #def ready(self):
        # sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/..')
        # # Set up Firebase credentials
        # script_path = os.path.dirname(os.path.abspath(__file__))
        # credentials_path = os.path.join(script_path, "credentials.json")
        # os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = credentials_path

        # # Initialize Firebase Admin SDK
        # try:
        #     firebase_admin
        # except NameError:
        #     cred = credentials.Certificate(credentials_path)
        #     firebase_admin = initialize_app(cred)

        # # Initialize Firestore client
        # db = firestore.Client()
        
        
        # #Delete all models in backend
        # Inventory.objects.all().delete()
        # Marketplace.objects.all().delete()
        # Suppliers.objects.all().delete()
        # Predictions.objects.all().delete()
        
        # update_model_from_firestore(Inventory, "Inventory")