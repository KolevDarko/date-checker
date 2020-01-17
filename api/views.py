from django.shortcuts import render

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from api.serializers import *


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class StoreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Store.objects.all()
    serializer_class = StoreSerializer

class ProductInStoreViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = ProductInStore.objects.all()
    serializer_class = ProductInStoreSerializer

