from rest_framework import serializers

from api.models import Category


class RecursiveField(serializers.Serializer):
    """
    A Serializer that recursively serializes any object.

    This is useful when you have a nested structure of objects, and you want to
    serialize the entire tree of objects in one go.

    The to_representation method is overridden to recursively call the serializer
    on each object in the tree.
    """

    def to_representation(self, value):
        """
        Recursively serialize the object and its children.

        Args:
            value (object): The object to be serialized.

        Returns:
            dict: The serialized object.
        """
        serializer = self.parent.parent.__class__(value, context=self.context)
        return serializer.data


class CategorySerializer(serializers.ModelSerializer):
    """
        Serializer for the Category model.

        Serializes the fields 'id', 'name', 'children', and 'parent' of the Category model.
        The 'children' field is a recursive field that serializes child categories.
        """
    children = RecursiveField(many=True, read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'children', 'parent']
        read_only_fields = ['id', 'children']
