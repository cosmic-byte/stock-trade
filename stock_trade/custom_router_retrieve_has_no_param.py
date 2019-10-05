from rest_framework.routers import DynamicRoute, Route, SimpleRouter


class CustomRouterRetrieveHasNoParam(SimpleRouter):
    routes = [

        # Detail route.
        Route(
            url=r'^/{prefix}$',
            mapping={
                'get': 'retrieve',
                'put': 'update',
                'patch': 'partial_update',
                'delete': 'destroy'
            },
            name='{basename}-detail',
            detail=True,
            initkwargs={'suffix': 'Instance'}
        ),

        Route(
            url=r'^/{prefix}/create$',
            mapping={
                'post': 'create'
            },
            name='{basename}-create',
            detail=False,
            initkwargs={'suffix': 'Create'}
        ),

        Route(
            url=r'^/{prefix}/list$',
            mapping={
                'get': 'list',
            },
            name='{basename}-list',
            detail=False,
            initkwargs={'suffix': 'List'}
        ),

        # Dynamically generated list routes. Generated using
        # @action(detail=False) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^/{prefix}/{url_path}$',
            name='{basename}-{url_name}',
            detail=False,
            initkwargs={}
        ),
        # Dynamically generated detail routes. Generated using
        # @action(detail=True) decorator on methods of the viewset.
        DynamicRoute(
            url=r'^/{prefix}/{lookup}/{url_path}$',
            name='{basename}-{url_name}',
            detail=True,
            initkwargs={}
        ),
    ]
