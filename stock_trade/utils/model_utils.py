from stock_trade.utils.custom_exceptions import ModelNotFoundException


def _get_queryset(klass):
    # If it is a model class or anything else with ._default_manager
    if hasattr(klass, '_default_manager'):
        return klass._default_manager.all()
    return klass


def _validate_queryset(klass, queryset):
    if not hasattr(queryset, 'get'):
        klass__name = klass.__name__ if isinstance(klass, type) else klass.__class__.__name__
        raise ValueError(
            "First argument must be a Model, Manager, "
            "or QuerySet, not '%s'." % klass__name
        )


def _format_dict(table):
    table_str = ''
    for k, v in table.items():
        table_str += f'{str(k)} = {str(v)} '
    return table_str


def get_object_or_400(klass, error_message=None, **kwargs):
    queryset = _get_queryset(klass)
    _validate_queryset(klass, queryset)
    try:
        return queryset.get(**kwargs)
    except queryset.model.DoesNotExist:
        if error_message:
            message = error_message
        else:
            message = f'{queryset.model._meta.object_name} with {_format_dict(kwargs)} was not found'
        raise ModelNotFoundException(message)


def get_object_or_none(klass, **kwargs):
    queryset = _get_queryset(klass)
    _validate_queryset(klass, queryset)
    try:
        return queryset.get(**kwargs)
    except (queryset.model.DoesNotExist, KeyError):
        return None

