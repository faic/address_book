import json

from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework.test import APIClient


class AddressesTest(APITestCase):

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

    def test_addresses_retrieve_initial_empty(self):
        response = self.client.get(
            '/addresses/',
        )
        assert response.status_code == status.HTTP_200_OK
        data = json.loads(response.content)
        assert 'results' in data
        assert 'count' in data
        assert data['results'] == []
        assert data['count'] == 0

    def test_addresses_create(self):
        response = self.client.post(
            '/addresses/',
            {
                "name": "address 1",
                "country": "US",
                "state": "CA",
                "city": "Los Angeles",
                "postal_code": "90210",
                "address_1": "Beverly Hills",
                "email": "test_email001@gmail.com",
            },
            format='json'
        )
        assert response.status_code == status.HTTP_201_CREATED
        data = json.loads(response.content)
        assert 'id' in data

    def test_addresses_retrieve_persistent(self):
        response = self.client.post(
            '/addresses/',
            {
                "name": "address 1",
                "country": "US",
                "state": "CA",
                "city": "Los Angeles",
                "postal_code": "90210",
                "address_1": "Beverly Hills",
                "email": "test_email001@gmail.com",
            },
            format='json'
        )
        data = json.loads(response.content)
        address_id = data["id"]
        response = self.client.get(
            '/addresses/' + str(address_id) + '/',
        )
        assert status.is_success(response.status_code)
        data = json.loads(response.content)
        assert data["name"] == "address 1"
        assert data["country"] == "US"
        assert data["state"] == "CA"
        assert data["city"] == "Los Angeles"
        assert data["postal_code"] == "90210"
        assert data["address_1"] == "Beverly Hills"
        assert data["email"] == "test_email001@gmail.com"

    def test_addresses_update(self):
        response = self.client.post(
            '/addresses/',
            {
                "name": "address 1",
                "country": "US",
                "state": "CA",
                "city": "Los Angeles",
                "postal_code": "90210",
                "address_1": "Beverly Hills",
                "email": "test_email001@gmail.com",
            },
            format='json'
        )
        data = json.loads(response.content)
        address_id = data["id"]
        response = self.client.put(
            '/addresses/' + str(address_id) + '/',
            {
                "name": "address 1 updated",
                "country": "US",
                "state": "CA",
                "city": "Los Angeles",
                "postal_code": "90210",
                "address_1": "Beverly Hills",
                "address_2": "apt. 1",
                "email": "test_email002@gmail.com",
            },
            format='json'
        )
        assert response.status_code == status.HTTP_200_OK
        data = json.loads(response.content)
        assert data["name"] == "address 1 updated"
        assert data["country"] == "US"
        assert data["state"] == "CA"
        assert data["city"] == "Los Angeles"
        assert data["postal_code"] == "90210"
        assert data["address_1"] == "Beverly Hills"
        assert data["address_2"] == "apt. 1"
        assert data["email"] == "test_email002@gmail.com"

    def test_addresses_delete(self):
        response = self.client.post(
            '/addresses/',
            {
                "name": "address 1",
                "country": "US",
                "state": "CA",
                "city": "Los Angeles",
                "postal_code": "90210",
                "address_1": "Beverly Hills",
                "email": "test_email001@gmail.com",
            },
            format='json'
        )
        data = json.loads(response.content)
        address_id = data["id"]
        response = self.client.delete(
            '/addresses/' + str(address_id) + '/',
        )
        assert status.is_success(response.status_code)
        response = self.client.get(
            '/addresses/' + str(address_id) + '/',
        )
        assert status.is_client_error(response.status_code)

    def test_addresses_pagination(self):
        for i in range(30):
            self.client.post(
                '/addresses/',
                {
                    "name": "address " + str(i),
                    "country": "US",
                    "state": "CA",
                    "city": "Los Angeles",
                    "postal_code": "90210",
                    "address_1": "Beverly Hills " + str(i),
                },
                format='json'
            )
        response = self.client.get(
            '/addresses/',
        )
        assert response.status_code == status.HTTP_200_OK
        data = json.loads(response.content)
        assert 'results' in data
        assert 'count' in data
        assert 'next' in data
        assert data['count'] == 30
        assert len(data['results']) == 20

        ids_set = set()
        for address in data['results']:
            ids_set.add(address['id'])

        response = self.client.get(
            data['next']
        )
        assert response.status_code == status.HTTP_200_OK
        data = json.loads(response.content)
        assert 'results' in data
        assert 'count' in data
        assert 'next' in data
        assert data['count'] == 30
        assert len(data['results']) == 10
        for address in data['results']:
            ids_set.add(address['id'])
        assert len(ids_set) == 30

    def test_addresses_create_duplicate(self):
        self.client.post(
            '/addresses/',
            {
                "name": "address 1",
                "country": "US",
                "state": "CA",
                "city": "Los Angeles",
                "postal_code": "90210",
                "address_1": "Beverly Hills",
                "email": "test_email001@gmail.com",
            },
            format='json'
        )
        response = self.client.post(
            '/addresses/',
            {
                "name": "address 2",
                "country": "US",
                "state": "CA",
                "city": "Los Angeles",
                "postal_code": "90210",
                "address_1": "Beverly Hills",
                "email": "test_email001@gmail.com",
            },
            format='json'
        )
        assert status.is_client_error(response.status_code)
        data = json.loads(response.content)
        assert data['error'] == "Duplicated address"

    def test_addresses_create_invalid_country(self):
        response = self.client.post(
            '/addresses/',
            {
                "name": "address 1",
                "country": "Vineland",
                "state": "CA",
                "city": "Los Angeles",
                "postal_code": "90210",
                "address_1": "Beverly Hills",
                "email": "test_email001@gmail.com",
            },
            format='json'
        )
        assert status.is_client_error(response.status_code)

    def test_addresses_create_invalid_email(self):
        response = self.client.post(
            '/addresses/',
            {
                "name": "address 1",
                "country": "US",
                "state": "CA",
                "city": "Los Angeles",
                "postal_code": "90210",
                "address_1": "Beverly Hills",
                "email": "not-a-email",
            },
            format='json'
        )
        assert status.is_client_error(response.status_code)

    def test_addresses_create_multiple_users(self):
        self.client.post(
            '/addresses/',
            {
                "name": "address 1",
                "country": "US",
                "state": "CA",
                "city": "Los Angeles",
                "postal_code": "90210",
                "address_1": "Beverly Hills",
                "email": "test_email001@gmail.com",
            },
            format='json'
        )

        user = User.objects.create_user(username="test_user2", password="3", is_active=True)
        user.save()
        client2 = APIClient()
        response = client2.post(
            '/api/login', {
                "username": "test_user2",
                "password": "3",
            },
            format='json'
        )

        result = json.loads(response.content)
        token = result['token']
        client2.credentials(HTTP_AUTHORIZATION='Token ' + token)

        client2.post(
            '/addresses/',
            {
                "name": "other address 1",
                "country": "US",
                "state": "NY",
                "city": "New York",
                "postal_code": "10050",
                "address_1": "5th Avenue",
                "email": "test_email001@gmail.com",
            },
            format='json'
        )

        response = self.client.get(
            '/addresses/',
        )
        data = json.loads(response.content)
        assert data['count'] == 1
        assert data['results'][0]['name'] == "address 1"

        response = client2.get(
            '/addresses/',
        )
        data = json.loads(response.content)
        assert data['count'] == 1
        assert data['results'][0]['name'] == "other address 1"

    def test_addresses_retrieve_no_auth(self):
        client = APIClient()

        response = client.get(
            '/addresses/',
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
        response = client.post(
            '/addresses/',
            {
                "name": "other address 1",
                "country": "US",
                "state": "NY",
                "city": "New York",
                "postal_code": "10050",
                "address_1": "5th Avenue",
                "email": "test_email001@gmail.com",
            },
            format='json'
        )
        assert response.status_code == status.HTTP_403_FORBIDDEN
