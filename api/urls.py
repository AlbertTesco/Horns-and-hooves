from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api.api_views.cart import CartViewSet
from api.api_views.category import CategoryViewSet
from api.api_views.order import OrderViewSet
from api.api_views.product import ProductViewSet, ProductDetailView
from api.apps import ApiConfig

router = DefaultRouter()
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'products', ProductViewSet, basename='product')
router.register(r'cart', CartViewSet, basename='cart')
router.register(r'orders', OrderViewSet, basename='order')

app_name = ApiConfig.name

urlpatterns = [
    path('', include(router.urls)),
    path('product/<int:pk>/', ProductDetailView.as_view(), name='product-detail'),

]
