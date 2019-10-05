from django.contrib import admin

# Register your models here.
from stock_trade.apps.user import models


class AppAdminAdmin(admin.ModelAdmin):
    list_display = ('user', 'first_name', 'last_name', 'gender', 'created_by',)
    search_fields = ('user__email', 'created_by__email',)


admin.site.register(models.AppAdmin, AppAdminAdmin)
admin.site.register(models.User)