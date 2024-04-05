from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()


class CartViewTestCase(TestCase):
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

    def test_add_to_cart(self):
        # Получаем JWT-токен для аутентификации
        refresh = RefreshToken.for_user(self.user)

        data = {
            "product_id": 1
        }
        response = self.client.post('/cart/', data=data, content_type='application/json',
                                    HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        expected_json = {
            "id": 1,
            "user": 1,
            "items": [
                {
                    "id": 1,
                    "product": {
                        "id": 1,
                        "name": "Test Product",
                        "description": "This is a test product.",
                        "price": "10.00",
                        "categories": []
                    },
                    "product_id": 1,
                    "quantity": 1
                }
            ]
        }

        self.assertEqual(response.json(), expected_json)

    def test_get_cart(self):
        # Получаем JWT-токен для аутентификации
        refresh = RefreshToken.for_user(self.user)

        data = {
            "product_id": 1
        }
        response = self.client.post('/cart/', data=data, content_type='application/json',
                                    HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        get_response = self.client.get('/cart/', content_type='application/json',
                                       HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        expected_json = [{
            "id": 1,
            "user": 1,
            "items": [
                {
                    "id": 1,
                    "product": {
                        "id": 1,
                        "name": "Test Product",
                        "description": "This is a test product.",
                        "price": "10.00",
                        "categories": []
                    },
                    "product_id": 1,
                    "quantity": 1
                }
            ]
        }]

        self.assertEqual(get_response.json(), expected_json)

    def test_remove_item_from_cart(self):
        refresh = RefreshToken.for_user(self.user)

        data = {
            "product_id": 1
        }
        response = self.client.post('/cart/', data=data, content_type='application/json',
                                    HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        data_for_del = {
            "item_id": 1
        }

        get_response = self.client.delete('/cart/1/remove_item/', data=data_for_del, content_type='application/json',
                                          HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.assertEqual(get_response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_cart(self):
        refresh = RefreshToken.for_user(self.user)

        data = {
            "product_id": 1
        }
        response = self.client.post('/cart/', data=data, content_type='application/json',
                                    HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        del_response = self.client.delete('/cart/1/', content_type='application/json',
                                          HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')

        self.assertEqual(del_response.status_code, status.HTTP_204_NO_CONTENT)