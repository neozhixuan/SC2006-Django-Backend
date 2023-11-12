from django.core.management.base import BaseCommand
from backend.views import update_model_from_firestore

class Command(BaseCommand):
    help = 'Update model from Firestore'

    def handle(self, *args, **options):
        update_model_from_firestore()
        self.stdout.write(self.style.SUCCESS('Successfully updated model from Firestore'))
