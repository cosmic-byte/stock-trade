from django.db import models
import uuid
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin

from .manager import UserManager


class User(PermissionsMixin, AbstractBaseUser):
    GENDER_MALE = 0
    GENDER_FEMALE = 1

    GENDER = (
        (GENDER_MALE, 'MALE'),
        (GENDER_FEMALE, 'FEMALE')
    )

    uid = models.UUIDField(
        unique=True,
        editable=False,
        default=uuid.uuid4,
        verbose_name='Public identifier',
    )
    email = models.EmailField(max_length=100, unique=True)
    email_verified = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'

    class Meta:
        verbose_name_plural = "users"

    def __str__(self):
        return self.email

    objects = UserManager()


class AppAdmin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='created_by', null=True)
    first_name = models.CharField(max_length=20, blank=True)
    last_name = models.CharField(max_length=20, blank=True)
    gender = models.IntegerField(choices=User.GENDER, null=True)
    deleted = models.BooleanField(default=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.first_name
