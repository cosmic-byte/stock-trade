from rest_framework.pagination import (
    LimitOffsetPagination,
    PageNumberPagination,
)


class ELimitPagination(LimitOffsetPagination):
    default_limit = 10
    max_limit = 50


class EPageNumberPagination(PageNumberPagination):
    page_size = 10
