import factory
from factory import post_generation

from stock_trade.apps.user.models import User, StockTradeUser


class UserFactory(factory.DjangoModelFactory):
    email = factory.Sequence(lambda n: 'person{0}@example.com'.format(n))

    @post_generation
    def password(self, create, extracted, **kwargs):
        self.set_password('password')

    class Meta:
        model = User


class AppAdminFactory(factory.DjangoModelFactory):
    first_name = 'App'
    last_name = 'Admin'
    user = factory.SubFactory(UserFactory)

    class Meta:
        model = StockTradeUser

