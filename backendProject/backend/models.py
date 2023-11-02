from django.contrib.auth.models import AbstractUser
from django.db import models

class Inventory(models.Model):

    def getOrders(self):
        return self.orders.all()

class OrderData(models.Model):
    ItemName = models.CharField(max_length=100)
    Quantity = models.PositiveIntegerField()
    FlowRate = models.PositiveIntegerField()
    ExpiryDate = models.DateField()
    EntryDate = models.DateField(auto_now_add = True)
    FoodCategory = models.CharField(max_length=50)
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='orders')
    
    def __str__(self):
        return f"{self.ItemName}"
        
class Suggestions(models.Model):
    SuggestionList = models.ManyToManyField('OrderData', related_name='suggested_lists')
    ItemName = models.CharField(max_length=64)

class Predictions(models.Model):
    PredictedStockLevel = models.ManyToManyField('OrderData', related_name='predicted_stock_levels')
    ConfidenceScore = models.IntegerField()
