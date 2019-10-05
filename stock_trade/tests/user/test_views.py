import pytest
from django.urls import reverse
from rest_framework import status

from stock_trade.tests.utils import authenticate_user


class TestAppAdminView:

    @pytest.mark.django_db
    def test_create_app_admin_by_anonymous_should_fail(self, api_client):
        payload = {
            'first_name': 'owner',
            'last_name': 'owner',
            'gender': 0,
            'user': {
                'email': 'ownerx@example.com',
                'password': 'password',
            }
        }
        url = reverse('app_admin-create')
        response = api_client.post(url, payload, format='json')

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    @pytest.mark.django_db
    def test_create_app_admin_by_admin_success(self, app_admin, api_client):
        client = authenticate_user(api_client, app_admin.user, admin_user=True)
        payload = {
            'first_name': 'owner',
            'last_name': 'owner',
            'gender': 0,
            'user': {
                'email': 'ownerx@example.com',
                'password': 'password',
            }
        }
        url = reverse('app_admin-create')
        response = client.post(url, payload, format='json')

        assert response.status_code == status.HTTP_201_CREATED
        assert len(response.data) == 4

