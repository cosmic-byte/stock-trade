import pytest
from random import random

from stock_trade.apps.user.models import User
from stock_trade.tests.user.factories import UserFactory, AppAdminFactory


@pytest.fixture
def random_email():
    return 'email{}@email.com'.format(random())


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
