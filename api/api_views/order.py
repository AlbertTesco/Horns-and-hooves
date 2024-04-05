from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from api.models import Order, Cart, OrderItem
from api.serializers.order import OrderSerializer


class OrderViewSet(ModelViewSet):
    """
    API endpoint that allows orders to be viewed or edited.
    """
    serializer_class = OrderSerializer
    queryset = Order.objects.all()

    def get_queryset(self):
        """
        Filter orders by the authenticated user.
        """
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)
        return self.queryset.none()

    def create(self, request, *args, **kwargs):
        """
        Create a new order.
        """
        if request.user.is_authenticated:
            cart = Cart.objects.filter(user=self.request.user).first()
            if not cart or not cart.cartitem_set.exists():
                return Response({"detail": "Cart is empty."}, status=status.HTTP_400_BAD_REQUEST)

            if not cart:
                return Response({"detail": "Cart not found."}, status=status.HTTP_404_NOT_FOUND)

            order = Order.objects.create(user=self.request.user)

            for item in cart.cartitem_set.all():
                OrderItem.objects.create(order=order, product=item.product, quantity=item.quantity)

            cart.cartitem_set.all().delete()

            order.total_price = sum(item.product.price * item.quantity for item in order.orderitem_set.all())
            print(sum(item.product.price * item.quantity for item in order.orderitem_set.all()))
            order.save()

            return Response(OrderSerializer(order).data, status=status.HTTP_201_CREATED)
        return Response({"detail": "Authentication credentials were not provided."},
                        status=status.HTTP_401_UNAUTHORIZED)

    def destroy(self, request, *args, **kwargs):
        """
        Delete an order.
        """
        order_id = kwargs.get('pk')
        order = get_object_or_404(Order, id=order_id)
        self.check_object_permissions(self.request, order)
        order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def list(self, request, *args, **kwargs):
        """
        List all orders for the authenticated user.
        """
        if request.user.is_authenticated:
            order = self.get_queryset().filter(user=request.user)
            serializer = OrderSerializer(order, many=True)
            return Response(serializer.data)
        return Response({"detail": "Authentication credentials were not provided."},
                        status=status.HTTP_401_UNAUTHORIZED)

    def retrieve(self, request, *args, **kwargs):
        """
        Retrieve an order.
        """
        if request.user.is_authenticated:
            order_id = kwargs.get('pk')
            order = get_object_or_404(Order, pk=order_id)
            serializer = OrderSerializer(order)
            return Response(serializer.data)
        else:
            return Response({"detail": "Authentication credentials were not provided."},
                            status=status.HTTP_401_UNAUTHORIZED)
