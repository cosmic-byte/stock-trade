from random import randint

from rest_framework.test import APIClient

from stock_trade.tests.user.fixtures import *


@pytest.fixture
def random_id(n):
    range_start = 10 ** (n - 1)
    range_end = (10 ** n) - 1
    return randint(range_start, range_end)


@pytest.fixture
def api_client():
    return APIClient()
