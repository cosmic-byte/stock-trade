from django.urls import path
from rest_framework_jwt.views import (
    ObtainJSONWebToken,
    RefreshJSONWebToken
)
from stock_trade.apps.user.views import (
    UserCreateView,
    EnableOrDisableUser,
    DeleteUserView, ActivateAccountView, AdminViewSet)
from stock_trade.auth import JWTSerializer, JWTRefreshTokenSerializer
from stock_trade.custom_router_retrieve_has_no_param import CustomRouterRetrieveHasNoParam

router = CustomRouterRetrieveHasNoParam()
router.register(r'admin', AdminViewSet, base_name='app_admin')


user_urls = [
        path('/create', UserCreateView.as_view(), name='create'),
        path('/activate_account/<str:uidb64>/<str:token>', ActivateAccountView.as_view(), name='activate-account'),
        path('/<uuid:uid>/delete', DeleteUserView.as_view(), name='delete'),
        path('/<uuid:uid>/enable-disable', EnableOrDisableUser.as_view(), name='enable-disable'),
        path('/login', ObtainJSONWebToken.as_view(serializer_class=JWTSerializer), name='login'),
        path('/api-token-refresh', RefreshJSONWebToken.as_view(serializer_class=JWTRefreshTokenSerializer), name='refresh')
]

urlpatterns = user_urls + router.urls
