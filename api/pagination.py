from rest_framework.pagination import PageNumberPagination


class CustomPagination(PageNumberPagination):
    """
    Custom pagination class that overrides the default page size.

    This class inherits from the built-in Django REST Framework
    `PageNumberPagination` class and overrides the default page size.
    The default page size is set to 10, but can be changed by specifying a
    different value for the `page_size` attribute. The maximum page size
    can also be set, to prevent unauthorized requests for extremely large
    result sets.

    Attributes:
        page_size (int): The number of items to include on each page.
        page_size_query_param (str): The query parameter used to specify the
            page size.
        max_page_size (int): The maximum number of items allowed in a page.
    """

    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100