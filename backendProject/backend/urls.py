from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path('api/orderdata/', views.OrderDataList.as_view(), name='orderdata-list'),
    path('api/orderdata/<int:pk>/',
         views.OrderDataDetail.as_view(), name='orderdata-detail'),
]
