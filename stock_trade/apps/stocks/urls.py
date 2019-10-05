from django.urls import path
from stock_trade.apps.stocks import views

urlpatterns = [
    path('/company-stock/<company_name>', views.GetCompanyStockView.as_view(),
         name='get-company-stock'),
]
