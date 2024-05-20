from typing import cast, Type

from litestar import Router, Controller
from litestar.exceptions import ImproperlyConfiguredException
from litestar.handlers import HTTPRouteHandler
from litestar.routes import BaseRoute, WebSocketRoute, ASGIRoute, HTTPRoute
from litestar.utils import join_paths, find_index, is_class_and_subclass, unique


class ControllerInstanceRouter(Router):
    def register(self, value: Controller | Type[Controller]) -> list[BaseRoute]:
        """
        This is an extension of the original code to allow for controller instances, specifically
        for controller instances that work on the HTTP protocol
        (idk if it will work for websockets or any other protocol)

        :param value: either a controller instance or controller type
        :return: BaseRoute

        Controller instances should not have objects that are not pickleable
        """

        validated_value = self._validate_controller_registration_value(value)

        routes: list[BaseRoute] = []

        for route_path, handlers_map in self.get_route_handler_map(value=validated_value).items():
            path = join_paths([self.path, route_path])
            if http_handlers := unique(
                    [handler for handler in handlers_map.values() if isinstance(handler, HTTPRouteHandler)]
            ):
                if existing_handlers := unique(
                        [
                            handler
                            for handler in self.route_handler_method_map.get(path, {}).values()
                            if isinstance(handler, HTTPRouteHandler)
                        ]
                ):
                    http_handlers.extend(existing_handlers)
                    existing_route_index = find_index(self.routes, lambda x: x.path == path)  # noqa: B023

                    if existing_route_index == -1:  # pragma: no cover
                        raise ImproperlyConfiguredException("unable to find_index existing route index")

                    route: WebSocketRoute | ASGIRoute | HTTPRoute = HTTPRoute(
                        path=path,
                        route_handlers=http_handlers,
                    )
                    self.routes[existing_route_index] = route
                else:
                    route = HTTPRoute(path=path, route_handlers=http_handlers)
                    self.routes.append(route)

                routes.append(route)

            if websocket_handler := handlers_map.get("websocket"):
                route = WebSocketRoute(path=path, route_handler=cast("WebsocketRouteHandler", websocket_handler))
                self.routes.append(route)
                routes.append(route)

            if asgi_handler := handlers_map.get("asgi"):
                route = ASGIRoute(path=path, route_handler=cast("ASGIRouteHandler", asgi_handler))
                self.routes.append(route)
                routes.append(route)

        return routes

    def _validate_controller_registration_value(self, value: Controller | Type[Controller]) -> Controller:
        if is_class_and_subclass(value, Controller):
            return value(owner=self)

        if isinstance(value, Controller):
            if value.owner == self:
                return value

        raise ImproperlyConfiguredException(
            "Unsupported value passed to `Router.register`. "
            "If you passed in a function or method, "
            "make sure to decorate it first with one of the routing decorators"
        )
