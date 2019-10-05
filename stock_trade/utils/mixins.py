from django.db.models import ProtectedError
from rest_framework import mixins

from stock_trade.utils import UnableToDeleteObject


class ErrorHandlingDestroyModelMixin(mixins.DestroyModelMixin):

    def perform_destroy(self, instance):
        try:
            instance.delete()
        except ProtectedError:
            raise UnableToDeleteObject
