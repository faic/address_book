import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APIClient, APITestCase


class LoginTests(APITestCase):

    def setUp(self):
        super().setUp()
        user = User.objects.create_user(username="test_user", password="2", is_active=True)
        user.save()
        self.client = APIClient()
        response = self.client.post(
            '/api/login', {
                "username": "test_user",
                "password": "2",
            },
            format='json'
        )

        result = json.loads(response.content)
        token = result['token']
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + token)

    def test_login_success(self):
        response = self.client.post(
            '/api/login', {
                "username": "test_user",
                "password": "2",
            },
            format='json'
        )
        assert status.is_success(response.status_code)
        data = json.loads(response.content)
        assert 'token' in data

    def test_login_no_credentials(self):
        response = self.client.post(
            '/api/login', {
                "f1": "v1",
                "f2": "v2",
            },
            format='json'
        )
        assert status.is_client_error(response.status_code)
        data = json.loads(response.content)
        assert 'error' in data
        assert data['error'] == 'No credentials provided'

    def test_login_invalid_credentials(self):
        response = self.client.post(
            '/api/login', {
                "username": "v1",
                "password": "v2",
            },
            format='json'
        )
        assert status.is_client_error(response.status_code)
        data = json.loads(response.content)
        assert 'error' in data
        assert data['error'] == 'Invalid Credentials'

    def test_login_same_token_relogin(self):
        response = self.client.post(
            '/api/login', {
                "username": "test_user",
                "password": "2",
            },
            format='json'
        )
        data = json.loads(response.content)
        token = data['token']

        response = self.client.post(
            '/api/login', {
                "username": "test_user",
                "password": "2",
            },
            format='json'
        )
        assert status.is_success(response.status_code)
        data = json.loads(response.content)
        assert token == data['token']
