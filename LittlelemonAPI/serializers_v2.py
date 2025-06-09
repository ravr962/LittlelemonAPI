# LittlelemonAPI/serializers_v2.py

from rest_framework import serializers
from .models import MenuItem, Order

class MenuItemV2Serializer(serializers.ModelSerializer):
    name = serializers.CharField(source='title')  # Rename field

    class Meta:
        model = MenuItem
        fields = ['id', 'name', 'price']  # Remove "inventory"

class MenuItemShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['title', 'price']  # hide 'inventory'
        
class OrderV2Serializer(serializers.ModelSerializer):
    menu_items = MenuItemShortSerializer(source='items', many=True, read_only=True)
    customer = serializers.CharField(source='customer_name')
    amount = serializers.DecimalField(source='total', max_digits=6, decimal_places=2)
    created_at = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer', 'menu_items', 'amount', 'created_at']

