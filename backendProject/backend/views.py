from django.shortcuts import render
from django.http import HttpResponse

from rest_framework import generics
from .models import OrderData
from .serializers import OrderDataSerializer


def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")


class OrderDataList(generics.ListCreateAPIView):
    queryset = OrderData.objects.all()
    serializer_class = OrderDataSerializer


class OrderDataDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = OrderData.objects.all()
    serializer_class = OrderDataSerializer
