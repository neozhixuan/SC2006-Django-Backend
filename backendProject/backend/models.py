from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import JSONField
from django.utils import timezone

class OrderData(models.Model):
    ItemName = models.CharField(max_length=100, default='default_value')
    Quantity = models.PositiveIntegerField(default=0)
    FlowRate = models.PositiveIntegerField(default=0)
    ExpiryDate = models.DateField(default=timezone.now)
    EntryDate = models.DateField(auto_now_add=True)
    #FoodCategory = models.CharField(max_length=50)
    #inventory = models.ForeignKey(
    #Inventory, on_delete=models.CASCADE, related_name='orders', null=True)

    def __str__(self):
        return f"{self.ItemName}"

class Inventory(models.Model):
    item_name = models.CharField(max_length=100, default='default_value')
    flow_rate = models.PositiveIntegerField(default=0)
    expiry_date = models.DateTimeField(default=timezone.now)
    quantity = models.PositiveIntegerField(default=0)
    entry_date = models.DateTimeField(default=timezone.now)

class Marketplace(models.Model):
    item_name = models.CharField(max_length=100, default='default_value')
    expiry_date = models.DateTimeField(default=timezone.now)
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

# class ABC(models.Model):
#     item_name = models.CharField(max_length=100, default='default_value')
#     price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

# class Suppliers(models.Model):
#     item_name = models.CharField(max_length=100, default='default_value')
#     flow_rate = models.PositiveIntegerField(default=0)
    
class Predictions(models.Model):
    items_data = models.JSONField(default=dict)

class Suggestions(models.Model):
    items_data = models.JSONField(default=dict)


