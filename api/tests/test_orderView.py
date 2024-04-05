from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class OrderViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpassword'
        )
        self.user.is_superuser = True
        self.user.is_active = True
        self.user.is_staff = True
        self.user.save()
        self.client.force_login(self.user)

        self.product = {
            'name': 'Test Product',
            'description': 'This is a test product.',
            'price': 10.00,
            "categories": []
        }

        self.client.post('/products/', data=self.product, content_type='application/json')

        refresh = RefreshToken.for_user(self.user)

        data = {
            "product_id": 1
        }
        self.client.post('/cart/', data=data, content_type='application/json',
                         HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

    def test_create_order(self):
        response = self.client.post('/orders/', content_type='application/json',
                                    HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(self.user).access_token}')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Проверяем, что ответ содержит необходимые поля и их типы данных
        expected_fields = {
            'id': int,
            'user': int,
            'items': list,
            'total_price': str,
        }

        for field, expected_type in expected_fields.items():
            with self.subTest(field=field):
                self.assertIn(field, response.json())
                self.assertIsInstance(response.json()[field], expected_type)

        # Проверяем, что каждый элемент списка items содержит необходимые поля и их типы данных
        for item in response.json()['items']:
            expected_item_fields = {
                'id': int,
                'product': dict,
                'quantity': int,
            }

            for field, expected_type in expected_item_fields.items():
                with self.subTest(field=field):
                    self.assertIn(field, item)
                    self.assertIsInstance(item[field], expected_type)

            # Проверяем, что внутренний словарь product содержит необходимые поля и их типы данных
            product = item['product']
            expected_product_fields = {
                'id': int,
                'name': str,
                'description': str,
                'price': str,
                'categories': list,
            }

            for field, expected_type in expected_product_fields.items():
                with self.subTest(field=field):
                    self.assertIn(field, product)
                    self.assertIsInstance(product[field], expected_type)

            # Проверяем состояние корзины после создания заказа
            cart_response = self.client.get('/cart/', content_type='application/json',
                                            HTTP_AUTHORIZATION=f'Bearer {RefreshToken.for_user(self.user).access_token}')
            self.assertEqual(cart_response.status_code, status.HTTP_200_OK)
            expected_cart_state = [
                {
                    "id": 1,
                    "user": 1,
                    "items": []
                }
            ]

            self.assertEqual(cart_response.json(), expected_cart_state)
