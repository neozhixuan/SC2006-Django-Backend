from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    # Functions called by controller classes
    path('fn/expiringFoods', views.filterForLowStock, name="filterForLowStock"),
    path('fn/getItemNames', views.getItemNames, name="getItemNames"),
    path('fn/createOrderData/', views.createOrderData, name='createOrderData'),

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
]
