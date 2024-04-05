from rest_framework import serializers
from api.models import Product, Category


class ProductWriteSerializer(serializers.ModelSerializer):
    """
    A Serializer for writing Product objects.
    """
    categories = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Category.objects.all()
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'categories')
        read_only_fields = ('id',)


class ProductReadSerializer(serializers.ModelSerializer):
    """
    A Serializer for reading Product objects.

    This Serializer includes the fields 'id', 'name', 'description', 'price', and 'categories',
    where 'categories' is a list of Category objects, each represented by their 'name' field.
    The 'categories' field is read-only.
    """

    categories = serializers.SlugRelatedField(
        many=True,
        read_only=True,
        slug_field='name'
    )

    class Meta:
        model = Product
        fields = ('id', 'name', 'description', 'price', 'categories')
        read_only_fields = ('id',)
