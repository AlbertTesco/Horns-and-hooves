from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets, status
from rest_framework.response import Response

from api.models import Cart, CartItem
from api.serializers.cart import CartSerializer, CartItemSerializer
from rest_framework.decorators import action


class CartViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows carts to be viewed or edited.
    """
    serializer_class = CartSerializer
    queryset = Cart.objects.all()

    def get_queryset(self):
        """
        Filter the carts returned based on the authenticated user.
        """
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)
        return self.queryset.none()

    def update(self, request, *args, **kwargs):
        """
        Update a cart.
        """
        if request.user.is_authenticated:
            cart = self.get_object()
            if cart.user != request.user:
                return Response({"detail": "You do not have permission to update this cart."},
                                status=status.HTTP_403_FORBIDDEN)

            # Update the cart
            serializer = CartSerializer(cart, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Update the cart items
            cart_items_data = request.data.get('items', [])
            for item_data in cart_items_data:
                item_id = item_data.get('id')
                try:
                    item = CartItem.objects.get(id=item_id, cart=cart)
                    serializer = CartItemSerializer(item, data=item_data, partial=True)
                    if serializer.is_valid():
                        serializer.save()
                    else:
                        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
                except CartItem.DoesNotExist:
                    return Response({"detail": "Cart item not found."}, status=status.HTTP_404_NOT_FOUND)

            return Response(serializer.data)
        return Response({"detail": "Authentication credentials were not provided."},
                        status=status.HTTP_401_UNAUTHORIZED)

    def create(self, request, *args, **kwargs):
        """
        Add an item to a cart.
        """
        if request.user.is_authenticated:
            serializer = CartItemSerializer(data=request.data)
            if serializer.is_valid():
                cart, _ = Cart.objects.get_or_create(user=request.user)
                product = serializer.validated_data['product']
                quantity = serializer.validated_data['quantity']
                cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
                if not created:
                    cart_item.quantity += quantity
                    cart_item.save()
                return Response(CartSerializer(cart).data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({"detail": "Authentication credentials were not provided."},
                        status=status.HTTP_401_UNAUTHORIZED)

    @swagger_auto_schema(
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'item_id': openapi.Schema(type=openapi.TYPE_INTEGER, description='ID of the item to remove'),
            },
            required=['item_id']
        ),
        responses={
            204: 'Item removed successfully',
            401: 'Authentication credentials were not provided',
            403: 'You do not have permission to remove this item',
            404: 'Item not found in cart',
        }
    )
    @action(detail=True, methods=['delete'])
    def remove_item(self, request, pk=None):
        """
        Remove an item from a cart.
        """
        if request.user.is_authenticated:
            cart = self.get_object()
            item_id = request.data.get('item_id')
            try:
                item = CartItem.objects.get(id=item_id, cart=cart)
                if item.cart.user != request.user:
                    return Response({"detail": "You do not have permission to remove this item."},
                                    status=status.HTTP_403_FORBIDDEN)
                item.delete()
                return Response(status=status.HTTP_204_NO_CONTENT)
            except CartItem.DoesNotExist:
                return Response({"detail": "Item not found in cart."}, status=status.HTTP_404_NOT_FOUND)
        return Response({"detail": "Authentication credentials were not provided."},
                        status=status.HTTP_401_UNAUTHORIZED)

    def list(self, request, *args, **kwargs):
        """
        Retrieve a list of carts.
        """
        if request.user.is_authenticated:
            cart = self.get_queryset().filter(user=request.user)
            serializer = CartSerializer(cart, many=True)
            return Response(serializer.data)
        return Response({"detail": "Authentication credentials were not provided."},
                        status=status.HTTP_401_UNAUTHORIZED)
