from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class ProductViewTestCase(TestCase):
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

    def test_create_product_view(self):
        data = {
            'name': 'Test Product',
            'description': 'This is a test product.',
            'price': 10.00,
            "categories": []
        }

        response = self.client.post('/products/', data=data, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        expected_json = {
            'id': response.json()['id'],
            'name': 'Test Product',
            'description': 'This is a test product.',
            'price': '10.00',
            "categories": []
        }

        self.assertEqual(response.json(), expected_json)

    def test_delete_product_view(self):
        data = {
            'name': 'Test Product',
            'description': 'This is a test product.',
            'price': 10.00,
            "categories": []
        }
        response = self.client.post('/products/', data=data, content_type='application/json')
        self.product_id = response.json()['id']

        del_response = self.client.delete(f'/products/{self.product_id}/')

        self.assertEqual(
            del_response.status_code,
            status.HTTP_204_NO_CONTENT
        )

    def test_retrieve_product_view(self):
        data = {
            'name': 'Test Product',
            'description': 'This is a test product.',
            'price': 10.00,
            "categories": []
        }
        response = self.client.post('/products/', data=data, content_type='application/json')
        self.product_id = response.json()['id']

        expected_json = {
            "id": 1,
            'name': 'Test Product',
            'description': 'This is a test product.',
            'price': '10.00',
            "categories": []
        }

        get_response = self.client.get(f'/products/{self.product_id}/')

        self.assertEqual(get_response.json(), expected_json)
