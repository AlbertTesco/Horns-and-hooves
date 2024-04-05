import django_filters
from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.views import APIView

from api.models import Product, Category
from api.pagination import CustomPagination
from api.serializers.product import ProductReadSerializer, ProductWriteSerializer


class ProductFilter(django_filters.FilterSet):
    """
    FilterSet for the Product model.
    """

    min_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="gte"
    )
    max_price = django_filters.NumberFilter(
        field_name="price", lookup_expr="lte"
    )

    class Meta:
        model = Product
        fields = ["min_price", "max_price"]


class ProductViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows products to be viewed or edited.
    """
    queryset = Product.objects.all()
    pagination_class = CustomPagination
    filterset_class = ProductFilter

    def get_serializer_class(self):
        """
        Return the appropriate serializer class based on the request method.
        """
        if self.action in ['list', 'retrieve']:
            return ProductReadSerializer
        else:
            return ProductWriteSerializer

    def get_queryset(self):
        """
        Filter the products based on the request parameters.
        """
        queryset = super().get_queryset()
        queryset = self.filter_queryset(queryset)
        category_id = self.request.query_params.get('category_id')
        if category_id:
            queryset = queryset.filter(categories__id=category_id)
        return queryset.order_by('id')

    def list(self, request):
        """
        Return a list of products.
        """
        queryset = self.get_queryset()
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)



class ProductDetailView(APIView):
    def get(self, request, pk):
        print(f"Received GET request for product with pk={pk}")
        try:
            product = Product.objects.get(pk=pk)
        except Product.DoesNotExist:
            print(f"Product with pk={pk} not found")
            return Response({"detail": "Product not found."}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductReadSerializer(product)
        return Response(serializer.data)
