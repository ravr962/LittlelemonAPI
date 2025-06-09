# Inside LittlelemonAPI/views_v2.py

from rest_framework import viewsets
from .models import MenuItem, Order
from .serializers_v2 import MenuItemV2Serializer, OrderV2Serializer

class MenuItemV2ViewSet(viewsets.ModelViewSet):
    queryset = MenuItem.objects.all()
    serializer_class = MenuItemV2Serializer


class OrderV2ViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderV2Serializer
