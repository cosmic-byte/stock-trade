from django.db import models

# Create your models here.
from stock_trade.apps.stocks.manager import CompanyStockManager


class CompanyStock(models.Model):

    company_name = models.CharField(max_length=20, blank=True)
    symbol = models.CharField(max_length=20, blank=True)
    primary_exchange = models.CharField(max_length=20, blank=True)
    calculation_price = models.CharField(max_length=20, blank=True)
    open = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    open_time = models.DateTimeField(auto_now=False, blank=True)
    close = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    close_time = models.DateTimeField(auto_now=False, blank=True)
    high = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    low = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    latest_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    latest_source = models.CharField(max_length=20, blank=True)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    objects = CompanyStockManager()

    def __str__(self):
        return "{} - {}".format(self.company_name, self.latest_price)

