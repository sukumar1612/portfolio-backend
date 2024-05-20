from litestar import Controller
from typing import Type

from litestar.exceptions import ImproperlyConfiguredException
from litestar.utils import is_class_and_subclass

from core.controller_instance_router import ControllerInstanceRouter


class HTTPApiController:
    def __init__(self, controller: Type[Controller], base_prefix: str, **kwargs):
        """
        :param controller: controller type
        :param base_prefix: any base path
        :param kwargs: any arguments to initialize the Controller

        this class is to initialize controllers inside the Application Container (basically for dependency injection)
        """
        if is_class_and_subclass(controller, Controller):
            self.router = ControllerInstanceRouter(path=base_prefix, route_handlers=[])
            kwargs['owner'] = self.router
            self.controller = controller(**kwargs)
            self.router.register(self.controller)
        else:
            raise ImproperlyConfiguredException("controller is not an instance of Controller")
