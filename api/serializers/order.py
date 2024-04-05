from rest_framework import serializers

from api.models import OrderItem, Order
from api.serializers.product import ProductReadSerializer


class OrderItemSerializer(serializers.ModelSerializer):
    """
    Serializer for OrderItem model.
    """
    product = ProductReadSerializer(read_only=True)

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    """
    Serializer for Order model.

    Attributes:
        id (int): Order ID.
        user (User): User who placed the order.
        items (list of OrderItem): List of order items.
        total_price (DecimalField): Total price of the order.
        created_at (DateTimeField): Time when the order was created.
    """

    items = OrderItemSerializer(source='orderitem_set', many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'total_price', 'created_at']
        read_only_fields = ['id', 'user', 'items', 'total_price', 'created_at']
