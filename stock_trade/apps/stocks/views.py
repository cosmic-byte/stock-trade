# Create your views here.
from rest_framework.generics import RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from stock_trade.apps.stocks.models import CompanyStock
from stock_trade.apps.stocks.serializer import RetrieveCompanyStockSerializer
from stock_trade.permissions import CustomDjangoModelPermissions
from stock_trade.utils.model_utils import camel_to_snake


class GetCompanyStockView(RetrieveAPIView):
    """
    Endpoint for retrieving a company's stock details
    """
    permission_classes = (CustomDjangoModelPermissions,)
    serializer_class = RetrieveCompanyStockSerializer
    queryset = CompanyStock.objects.all()

    def get(self, request, *args, **kwargs):
        company_name = kwargs.get('company_name')
        company_stock = self.serializer_class.get_stock(company_name)
        if company_stock:
            for key in company_stock.keys():
                company_stock[camel_to_snake(key)] = company_stock.pop(key)
            company_stock = self.serializer_class(company_stock)
            return Response(company_stock.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)
