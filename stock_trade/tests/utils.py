from django.urls import reverse
from rest_framework_jwt.serializers import JSONWebTokenSerializer
from rest_framework.test import APIClient

from stock_trade.apps.user.models import User


def authenticate_user(client, user, admin_user=False):
    if admin_user:
        user.is_superuser = True
        user.save()
    url = reverse('login')
    response = client.post(url, data={
        'email': user.email,
        'password': "password"
    })
    token = response.data.get('token', None)
    client.credentials(HTTP_AUTHORIZATION='Bearer {}'.format(token))
    return client


def get_authenticated_user_client():
    client = APIClient()
    User.objects.create_user(email="inem.patrick@gmail.com", password="password")
    serializer = JSONWebTokenSerializer()
    attrs = {
        'email': 'inem.patrick@gmail.com',
        'password': 'password',
    }
    user_credential = serializer.validate(attrs)
    client.credentials(HTTP_AUTHORIZATION='Bearer ' + user_credential.get('token'))
    return client
