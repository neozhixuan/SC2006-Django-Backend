from django.urls import path
from django.contrib import admin
from django.urls import include, path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Functions called by controller classes
    path('fn/expiringFoods', views.filterForExpiringStock,
         name="filterForLowStock"),
    path('fn/getItemNames', views.getItemNames, name="getItemNames"),

    # POST Requests
    path('fn/createOrderData/', views.createOrderData, name='createOrderData'),
    path('fn/createSuggestion/', views.createSuggestion, name='createSuggestions'),
    path('fn/createPrediction/', views.createPrediction, name='createPredictions'),
    path('fn/createSupplier/', views.createSupplier, name='createSupplier'),

    # REST API URLS
    path('api/orderdata/', views.OrderDataList.as_view(), name='orderdata-list'),
    path('api/orderdata/<int:pk>/',
         views.OrderDataDetail.as_view(), name='orderdata-detail'),
    path('api/suggestions/', views.SuggestionsList.as_view(),
         name='suggestions-list'),
    path('api/suggestions/<int:pk>/',
         views.SuggestionsDetail.as_view(), name='suggestions-detail'),
    path('api/predictions/', views.PredictionsList.as_view(),
         name='predictions-list'),
    path('api/predictions/<int:pk>/',
         views.PredictionsDetail.as_view(), name='predictions-detail'),
    path('api/supplier/', views.SupplierList.as_view(), name='supplier-list'),
     
     path('index/',views.index,name='test'),
     
     # Firebase Connection
     path('view_firestore_data/', views.view_firestore_data, name='view_firestore_data')
]
