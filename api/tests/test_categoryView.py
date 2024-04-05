from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from rest_framework import status

User = get_user_model()


class CategoryViewTestCase(TestCase):
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

    def test_create_category_view(self):
        category = {
            'name': 'Test Category'
        }

        response = self.client.post('/categories/', data=category, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        expected_json = {
            'id': response.json()['id'],
            'name': 'Test Category',
            "children": [],
            "parent": None
        }

        self.assertEqual(response.json(), expected_json)

        subcategory = {
            'name': 'Test Subcategory',
            'parent': 1
        }

        response = self.client.post('/categories/', data=subcategory, content_type='application/json')

        expected_json = {
            'id': response.json()['id'],
            'name': 'Test Subcategory',
            "children": [],
            "parent": 1
        }

        self.assertEqual(response.json(), expected_json)

    def test_list_category_view(self):
        category = {
            'name': 'Test Category'
        }

        self.client.post('/categories/', data=category, content_type='application/json')

        response = self.client.get('/categories/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_json = [
            {
                'id': 1,
                'name': 'Test Category',
                "children": [],
                "parent": None
            }
        ]

        self.assertEqual(response.json(), expected_json)

    def test_retrieve_category_view(self):
        category = {
            'name': 'Test Category'
        }

        self.client.post('/categories/', data=category, content_type='application/json')

        response = self.client.get('/categories/1/')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_json = {
            'id': 1,
            'name': 'Test Category',
            "children": [],
            "parent": None
        }

        self.assertEqual(response.json(), expected_json)

    def test_update_category_view(self):
        # Создаем категорию
        category = {
            'name': 'Test Category'
        }
        self.client.post('/categories/', data=category, content_type='application/json')

        updated_category = {
            'name': 'Updated Test Category'
        }
        response = self.client.put('/categories/1/', data=updated_category, content_type='application/json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        expected_json = {
            'id': 1,
            'name': 'Updated Test Category',
            "children": [],
            "parent": None
        }

        self.assertEqual(response.json(), expected_json)

        response = self.client.get('/categories/1/')
        self.assertEqual(response.json(), expected_json)

    def test_delete_category_view(self):
        category = {
            'name': 'Test Category'
        }
        self.client.post('/categories/', data=category, content_type='application/json')

        response = self.client.delete('/categories/1/')

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

        response = self.client.get('/categories/1/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
