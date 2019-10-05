from random import random, randint

import pytest
from rest_framework.test import APIClient

from stock_trade.apps.user.models import User
from stock_trade.tests.user.factories import UserFactory, AppAdminFactory


@pytest.fixture
def random_email():
    return 'email{}@email.com'.format(random())


@pytest.fixture
def random_id(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


@pytest.fixture
def user():
    return UserFactory()


@pytest.fixture
def app_admin(user):
    user = User.objects.create_app_admin_user(
        email=random_email(),
        password="password"
    )
    return AppAdminFactory(user=user)


@pytest.fixture
def api_client():
    return APIClient()
