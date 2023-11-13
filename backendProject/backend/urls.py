from django.urls import path
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    # Default Path
    path("", views.index, name="index"),

    ##########################
    # Functions called by controller classes
    ##########################
    path('fn/expiringFoods', views.filterForExpiringStock,
         name="filterForLowStock"),
    path('fn/getItemNames', views.getItemNames, name="getItemNames"),

    ##########################
    # POST Requests
    ##########################
    path('fn/createInventory/', views.createInventory, name='createInventory'),
    path('fn/createSuggestion/', views.createSuggestion, name='createSuggestions'),
    path('fn/createPrediction/', views.createPrediction, name='createPredictions'),
    path('fn/createSupplier/', views.createSupplier, name='createSupplier'),

    ##########################
    # REST API URLS
    ##########################
    path('api/inventory/', views.InventoryList.as_view(), name='inventory-list'),
    path('api/marketplace/', views.MarketplaceList.as_view(),
         name='marketplace-list'),
    path('api/suggestions/', views.SuggestionsList.as_view(),
         name='suggestions-list'),
    path('api/suggestions/<int:pk>/',
         views.SuggestionsDetail.as_view(), name='suggestions-detail'),
    path('api/predictions/', views.PredictionsList.as_view(),
         name='predictions-list'),
    path('api/predictions/<int:pk>/',
         views.PredictionsDetail.as_view(), name='predictions-detail'),
    path('api/supplier/', views.SupplierList.as_view(), name='supplier-list'),
]
