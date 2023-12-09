from calendly.factories import BaseFactory
from calendly.services import CalendlyService
from calendly.services.user_availability_service import UserAvailabilityService
from calendly.misc.constants import USER_SERVICE_KEY

class ServiceFactory(BaseFactory):

    @classmethod
    def create(cls, name: str) -> CalendlyService:
        if name == USER_SERVICE_KEY:
            return UserAvailabilityService()
        else:
            raise NotImplementedError(f"No service implemented for the key '{name}'.")
