from calendly.factories import BaseFactory
from calendly.rest import CalendlyRestInterface
from calendly.rest.user_controller import UserRestController
from calendly.misc.constants import USER_CONTROLLER_KEY

class ControllerFactory(BaseFactory):

    @classmethod
    def create(cls, name: str) -> CalendlyRestInterface:
        if name == USER_CONTROLLER_KEY:
            return UserRestController()
        else:
            raise NotImplementedError(f"No controller implemented for the key '{name}'.")