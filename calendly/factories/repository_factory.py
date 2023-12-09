from calendly.factories import BaseFactory
from calendly.repositories import CalendlyRepository
from calendly.repositories.user_repository import UserRepository
from calendly.repositories.user_hourly_slot_availability_repository import UserHourlySlotAvailabilityRepository
from calendly.misc.constants import USER_REPOSITORY_KEY, USER_HOURLY_SLOT_AVAILABILITY_REPOSITORY_KEY

class RepositoryFactory(BaseFactory):

    @classmethod
    def create(cls, name: str) -> CalendlyRepository:
        if name == USER_REPOSITORY_KEY:
            return UserRepository()
        elif name == USER_HOURLY_SLOT_AVAILABILITY_REPOSITORY_KEY:
            return UserHourlySlotAvailabilityRepository()
        else:
            raise NotImplementedError(f"No repository implemented for the key '{name}'.")
