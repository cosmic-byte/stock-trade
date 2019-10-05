from datetime import datetime, timedelta
from pytz import timezone
from calendar import timegm

from rest_framework_jwt.settings import api_settings

from stock_trade.apps.user.serializer import UserRetrieveSerializer, RetrieveStockTradeUserSerializer
from django.contrib.auth import authenticate

from rest_framework import serializers
from rest_framework_jwt.serializers import (
    JSONWebTokenSerializer,
    RefreshJSONWebTokenSerializer,
    jwt_payload_handler,
    jwt_encode_handler
)

from stock_trade.apps.user.models import User


def get_logged_in_user_profile(user):
    try:
        return RetrieveStockTradeUserSerializer(user.stocktradeuser).data
    except (KeyError, TypeError):
        return None


class JWTSerializer(JSONWebTokenSerializer):
    username_field = 'email'

    def validate(self, attrs):
        password = attrs.get("password")
        user_obj = User.objects.filter(email=attrs.get("email")).first()
        if user_obj:
            credentials = {
                'username': user_obj.email,
                'password': password
            }
            if all(credentials.values()):
                user = authenticate(**credentials)
                if user:
                    if not user.is_active:
                        raise serializers.ValidationError('User account is disabled.')
                    if user.deleted:
                        raise serializers.ValidationError('User account is deleted.')
                    payload = jwt_payload_handler(user)
                    return {
                        'token': jwt_encode_handler(payload),
                        'user': user
                    }
                else:
                    raise serializers.ValidationError('Wrong log in credentials.')
            else:
                message = "Must include {username_field} and password".format(username_field=self.username_field)
                raise serializers.ValidationError(message)
        else:
            raise serializers.ValidationError('Account with this email/username does not exists')


class JWTRefreshTokenSerializer(RefreshJSONWebTokenSerializer):
    """
    Refresh an access token.
    """

    def validate(self, attrs):
        token = attrs['token']

        payload = self._check_payload(token=token)
        user = self._check_user(payload=payload)
        # Get and check 'orig_iat'
        orig_iat = payload.get('orig_iat')

        if orig_iat:
            # Verify expiration
            refresh_limit = api_settings.JWT_REFRESH_EXPIRATION_DELTA

            if isinstance(refresh_limit, timedelta):
                refresh_limit = (refresh_limit.days * 24 * 3600 +
                                 refresh_limit.seconds)

            expiration_timestamp = orig_iat + int(refresh_limit)
            now_timestamp = timegm(datetime.utcnow().utctimetuple())

            if now_timestamp > expiration_timestamp:
                msg = _('Refresh has expired.')
                raise serializers.ValidationError(msg)
        else:
            msg = _('orig_iat field is required.')
            raise serializers.ValidationError(msg)

        new_payload = jwt_payload_handler(user)
        new_payload['orig_iat'] = orig_iat

        return {
            'token': jwt_encode_handler(new_payload),
            'user': user,
            'token_exp_date': datetime.now(timezone('Africa/Lagos')) + api_settings.JWT_EXPIRATION_DELTA,
        }


def jwt_response_payload_handler(token, user=None, request=None):
    user_data = UserRetrieveSerializer(instance=user).data
    profile = get_logged_in_user_profile(user)
    if profile:
        user_data['profile'] = profile

        # Remove nested user from profile
        if profile.get('user'):
            _ = profile.pop('user')

    return {
        'token': token,
        'user': user_data,
        'token_exp_date': datetime.now(timezone('Africa/Lagos')) + api_settings.JWT_EXPIRATION_DELTA,
    }
