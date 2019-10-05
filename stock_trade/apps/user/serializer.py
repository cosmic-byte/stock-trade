from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from rest_framework import serializers

from stock_trade.apps.user.models import StockTradeUser

User = get_user_model()


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ('name',)


class UserCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'password',)

    def create(self, validated_data):
        user = User.objects.create_stock_trade_user(
            email=validated_data.pop('email'),
            password=validated_data.pop('password'),
            **validated_data
        )
        return user


class UserRetrieveSerializer(serializers.HyperlinkedModelSerializer):
    groups = GroupSerializer(many=True)

    class Meta:
        model = User
        fields = ('email', 'uid', 'groups', 'is_active')
        read_only_fields = ('groups',)


class UserListSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = User
        fields = ('email', 'uid')


class EnableDisableUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = []

    def update(self, instance, validated_data, **kwargs):
        instance.is_active = not instance.is_active
        instance.save()
        return instance


class DeleteUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = []

    def update(self, instance, validated_data, **kwargs):
        instance.deleted = not instance.deleted
        instance.save()
        return instance


class CreateStockUserSerializer(serializers.ModelSerializer):

    user = UserCreateSerializer()

    class Meta:
        model = StockTradeUser
        fields = ('first_name', 'last_name', 'gender', 'user',)

    def create(self, validated_data):
        user_to_create = validated_data.pop('user')
        user = User.objects.create_stock_trade_user(
            email=user_to_create['email'],
            password=user_to_create['password'],
        )
        stock_user = StockTradeUser.objects.create(
            user=user,
            **validated_data
        )
        return stock_user


class CreateAdminSerializer(serializers.ModelSerializer):

    user = UserCreateSerializer()

    class Meta:
        model = StockTradeUser
        fields = ('first_name', 'last_name', 'gender', 'user',)

    def create(self, validated_data):
        logged_in_user = self.context['request'].user
        user_to_create = validated_data.pop('user')
        user = User.objects.create_app_admin_user(
            email=user_to_create['email'],
            password=user_to_create['password'],
        )
        admin = StockTradeUser.objects.create(
            user=user,
            admin_created_by=logged_in_user,
            **validated_data
        )
        return admin


class RetrieveStockTradeUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = StockTradeUser
        fields = ('first_name', 'last_name', 'gender',)
