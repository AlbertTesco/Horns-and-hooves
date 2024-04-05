from django.contrib.auth.models import User
from django.db import models

NULLABLE = {
    'blank': True,
    'null': True,
}


class Category(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название категории')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name="children",
                               verbose_name="Родительская категория", **NULLABLE)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100, verbose_name='Название продукта')
    description = models.TextField(verbose_name='Описание продукта')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Цена продукта')
    categories = models.ManyToManyField(Category, related_name='products', verbose_name='Категория')

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'


class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    product = models.ManyToManyField(Product, through='CartItem', verbose_name='Продукт')

    class Meta:
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, verbose_name='Корзина')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1)

    class Meta:
        verbose_name = 'Элемент корзины'
        verbose_name_plural = 'Элементы корзины'


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    products = models.ManyToManyField(Product, through='OrderItem', verbose_name='Продукты')
    total_price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Общая стоимость', default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Продукт')
    quantity = models.PositiveIntegerField(verbose_name='Количество', default=1)

    class Meta:
        verbose_name = 'Элемент заказа'
        verbose_name_plural = 'Элементы заказа'
