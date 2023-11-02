from django.contrib.auth.models import AbstractUser
from django.db import models

class Inventory(models.Model):


class OrderData(models.Model):
    ItemName = models.CharField(max_length=100)
    Quantity = models.PositiveIntegerField()
    FlowRate = models.PositiveIntegerField()
    ExpiryDate = models.DateField()
    EntryDate = models.DateField()
    FoodCategory = models.CharField(max_length=50)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='orders')
    
    def __str__(self):
        return f"{self.ItemName}"
