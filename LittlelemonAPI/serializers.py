from rest_framework import serializers
from .models import Order, MenuItem

class MenuItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = MenuItem
        fields = ['id', 'title', 'price', 'inventory']
        
    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Price must be non-negative.")
        return value
    
    def validate_inventory(self, value):
        if value < 0:
            raise serializers.ValidationError("Inventory must be non-negative.")
        return value

class OrderSerializer(serializers.ModelSerializer):
    items = MenuItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'items', 'total', 'created_at']

class OrderCreateSerializer(serializers.Serializer):
    customer_name = serializers.CharField()
    item_ids = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=MenuItem.objects.all(),
        write_only=True
    )

    def validate(self, data):
        if not data.get('item_ids'):
            raise serializers.ValidationError("An order must include at least one menu item.")
        return data

    def create(self, validated_data):
        menu_items = validated_data.pop('item_ids')
        total = sum(item.price for item in menu_items)
        user = self.context['request'].user  # <- this is passed from the view

        order = Order.objects.create(
            customer_name=validated_data['customer_name'],
            total=total,
            user=user
        )
        order.items.set(menu_items)
        return order
    
    def to_representation(self, instance):
        return OrderSerializer(instance, context=self.context).data

class SimpleOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'items', 'total', 'created_at']
        read_only_fields = ['total', 'created_at']

    def create(self, validated_data):
        items = validated_data.pop('items')  # Extract related menu items
        total = sum(item.price for item in items)  # Calculate order total
        user = self.context['request'].user  # 👈 grab the user from the request
        order = Order.objects.create(user=user, total=total, **validated_data)  # Save order with total
        order.items.set(items)  # Assign menu items (M2M)
        return order


    # DRF handles related fields like items using primary key by default


# class OrderCreateSerializer(serializers.Serializer):
#     customer_name = serializers.CharField()
#     item_ids = serializers.ListField(child=serializers.IntegerField())

