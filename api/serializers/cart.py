from rest_framework import serializers

from api.models import CartItem, Cart, Product
from api.serializers.product import ProductReadSerializer


class CartItemSerializer(serializers.ModelSerializer):
    """
    CartItemSerializer class that defines the structure of a single cart item.

    Attributes:
        id (int): The unique ID of the cart item.
        product (ProductReadSerializer): The product information.
        product_id (int): The ID of the product.
        quantity (int): The quantity of the product in the cart.
    """

    product = ProductReadSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(),
        source='product',
        required=True
    )
    quantity = serializers.IntegerField(default=1, required=False)

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'product_id', 'quantity']
        extra_kwargs = {
            'product': {'read_only': True},
        }


class CartSerializer(serializers.ModelSerializer):
    """
    CartSerializer class that defines the structure of a cart.

    Attributes:
        id (int): The unique ID of the cart.
        user (User): The user information.
        items (List[CartItemSerializer]): The list of cart items.
    """

    items = CartItemSerializer(source='cartitem_set', many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ('id', 'user', 'items',)
