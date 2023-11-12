from django.contrib import admin
from .models import *


# @admin.register(OrderData)
# class OrderDataAdmin(admin.ModelAdmin):
#     list_display = ('ItemName', 'Quantity', 'FlowRate',
#                     'ExpiryDate', 'EntryDate', 'FoodCategory')

admin.site.register(OrderData)  # Register your model
admin.site.register(Suggestions)  # Register your model
admin.site.register(Predictions)  # Register your model
#admin.site.register(Suppliers)  # Register your model
admin.site.register(Inventory)  # Register your model
admin.site.register(Marketplace)  # Register your model
