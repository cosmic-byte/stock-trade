from rest_framework import serializers


from stock_trade.apps.stocks.models import CompanyStock
from stock_trade.utils.requests import IEXStockRequest


class RetrieveCompanyStockSerializer(serializers.ModelSerializer):

    class Meta:
        model = CompanyStock
        fields = '__all__'

    @staticmethod
    def get_stock(company_name):
        return IEXStockRequest().get_iex_stock_for_company(company_name)
