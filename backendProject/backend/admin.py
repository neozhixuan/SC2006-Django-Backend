from django.contrib import admin
from .models import *


# @admin.register(OrderData)
# class OrderDataAdmin(admin.ModelAdmin):
#     list_display = ('ItemName', 'Quantity', 'FlowRate',
#                     'ExpiryDate', 'EntryDate', 'FoodCategory')

admin.site.register(OrderData)  # Register your model
