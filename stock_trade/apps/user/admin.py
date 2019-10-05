from django.contrib import admin

# Register your models here.
from stock_trade.apps.user import models


class StockTradeUserAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'gender', 'admin_created_by',)
    search_fields = ('user__email', 'user__groups__first__name', 'created_by__email',)


admin.site.register(models.StockTradeUser, StockTradeUserAdmin)
admin.site.register(models.User)
