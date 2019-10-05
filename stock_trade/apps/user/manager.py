from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import Group
from rest_framework.generics import get_object_or_404


class UserManager(BaseUserManager):

    def create_base_user(self, email=None, password=None, **extra_fields):
        if not email or not password:
            raise ValueError('The email and password must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_app_admin_user(self, email=None, password=None, **extra_fields):
        admin_group = get_object_or_404(Group, name='app_admin')
        user = self.create_base_user(email=email, password=password, **extra_fields)
        user.groups.add(admin_group)
        return user

    def create_stock_trade_user(self, email=None, password=None, **extra_fields):
        stock_user_group = get_object_or_404(Group, name='stock_user')
        user = self.create_base_user(email=email, password=password, **extra_fields)
        user.groups.add(stock_user_group)
        return user

    def create_superuser(self, email, password, **extra_fields):
        user = self.create_base_user(email=email, password=password, **extra_fields)
        user.is_admin = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
