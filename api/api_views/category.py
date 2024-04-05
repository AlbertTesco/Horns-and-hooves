from rest_framework import viewsets
from rest_framework.response import Response

from api.models import Category
from api.serializers.category import CategorySerializer


class CategoryViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows categories to be viewed or edited.
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def list(self, request):
        """
        List all categories.
        """
        queryset = Category.objects.filter(parent=None)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)
