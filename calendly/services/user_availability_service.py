from calendly.services import CalendlyService
from typing import Optional
from calendly.dtos.user_availability_filter import UserAvailabilityFilter
from calendly.factories.repository_factory import RepositoryFactory
from calendly.misc.constants import USER_REPOSITORY_KEY, USER_HOURLY_SLOT_AVAILABILITY_REPOSITORY_KEY
from calendly.misc.exceptions import ObjectNotFoundException
from calendly.utils.datetime import tz_str_to_tz_obj
from calendly.dtos.availability_config import AvailabilityConfig, PerDateAvailabilityConfig, PatternBasedAvailabilityConfig
from calendly.entities.user_hourly_slot_availability import UserHourlySlotAvailability
from collections import defaultdict


class UserAvailabilityService(CalendlyService):
    def __init__(self):
        self.user_repo = RepositoryFactory.create(USER_REPOSITORY_KEY)
        self.user_hourly_slot_availability_repo = RepositoryFactory.create(USER_HOURLY_SLOT_AVAILABILITY_REPOSITORY_KEY)

    def get_availability(
        self, user_id: str, user_availability_filter: UserAvailabilityFilter, timezone: Optional[str] = None
    ) -> list[dict]:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ObjectNotFoundException(f"User not found with id {user_id}.")

        timezone = timezone if timezone else user.timezone
        if not user_availability_filter:
            raise ValueError("User availability filter not provided.")

        start_date, end_date = user_availability_filter.get_date_range(tz_str_to_tz_obj(timezone))
        # TODO: this only filters based on user input also add logic to filter out
        #  slots based on user's working days
        available_slots = self.user_hourly_slot_availability_repo.get_user_slots_in_date_range(user_id, start_date, end_date)

        return [available_slot.to_dict() for available_slot in available_slots]


    def set_availability(
        self, user_id: str, availability_config: AvailabilityConfig, timezone: Optional[str] = None
    ) -> None:
        user = self.user_repo.get_by_id(user_id)
        if not user:
            raise ObjectNotFoundException(f"User not found with id {user_id}.")

        timezone = timezone if timezone else user.timezone
        print("user: ", user)
        print("availability_config: ", availability_config)
        if not availability_config:
            # nothing to do
            return

        print("availability_config: ", availability_config)
        availability_slots_to_add = []
        availability_slots_to_update = []
        if isinstance(availability_config, PerDateAvailabilityConfig):
            for date_slot in availability_config.dates_slots:
                existing_date_slots = self.user_hourly_slot_availability_repo.filter(
                    [
                        {
                            "key": "user_id",
                            "value": user_id,
                            "op": "eq",
                        },
                        {
                            "key": "date",
                            "value": date_slot.date,
                            "op": "eq",
                        }
                    ]
                )
                slot_to_obj_map = {existing_date_slot.slot: existing_date_slot for existing_date_slot in existing_date_slots}
                for slot in date_slot.slots:
                    for slot_start in range(slot[0], slot[1]):
                        if slot_start not in slot_to_obj_map:
                            availability_slots_to_add.append(
                                UserHourlySlotAvailability(
                                    id=None,
                                    created_at=None,
                                    updated_at=None,
                                    created_by=user_id,
                                    last_updated_by=None,
                                    user_id=user_id,
                                    date=date_slot.date,
                                    slot=slot_start,
                                    available_duration=1,
                                )
                            )
                        elif slot_to_obj_map[slot_start].available_duration < 1:
                            slot_to_obj_map[slot_start].available_duration = 1
                            availability_slots_to_update.append(slot_to_obj_map[slot_start].available_duration)


            print("availability_slots_to_add: ", availability_slots_to_add)
            print("availability_slots_to_update: ", availability_slots_to_update)
            self.user_hourly_slot_availability_repo.add_in_bulk(availability_slots_to_add)
            self.user_hourly_slot_availability_repo.update_in_bulk(availability_slots_to_update)
        elif isinstance(availability_config, PatternBasedAvailabilityConfig):
            # Todo: Implment pattern based availability repetition
            raise NotImplementedError(f"Set up of availability based on {availability_config.__name__} is not yet implemented.")
        else:
            raise ValueError(f"Unsupported availability config type {availability_config.__name__}")

        return

    def get_overlapping_available_slots(
        self,
        user_id1: str,
        user_id2: str,
        user_availability_filter: UserAvailabilityFilter,
        timezone: Optional[str] = None,
    ) -> list[dict]:
        user1 = self.user_repo.get_by_id(user_id1)
        user2 = self.user_repo.get_by_id(user_id2)
        if not user1:
            raise ObjectNotFoundException(f"User not found with id {user_id1}.")
        if not user2:
            raise ObjectNotFoundException(f"User not found with id {user_id2}.")

        # consider user1 as primary user and use their timezone if not available
        timezone = timezone if timezone else user1.timezone
        if not user_availability_filter:
            raise ValueError("User availability filter not provided.")

        start_date, end_date = user_availability_filter.get_date_range(tz_str_to_tz_obj(timezone))

        # TODO: this only filters based on user input also add logic to filter out
        #  slots based on user's working days
        user1_available_slots = self.user_hourly_slot_availability_repo.get_user_slots_in_date_range(
            user_id1, start_date, end_date
        )
        user2_available_slots = self.user_hourly_slot_availability_repo.get_user_slots_in_date_range(
            user_id2, start_date, end_date
        )
        user1_date_to_slots = {}
        for date_slot in user1_available_slots:
            if date_slot.available_duration > 0:
                if str(date_slot.date) not in user1_date_to_slots:
                    day_slots = [0] * 23
                    user1_date_to_slots[str(date_slot.date)] = day_slots
                user1_date_to_slots[str(date_slot.date)][date_slot.slot] = date_slot.available_duration

        user2_date_to_slots = {}
        for date_slot in user2_available_slots:
            if date_slot.available_duration > 0:
                if str(date_slot.date) not in user2_date_to_slots:
                    day_slots = [0] * 23
                    user2_date_to_slots[str(date_slot.date)] = day_slots
                user2_date_to_slots[str(date_slot.date)][date_slot.slot] = date_slot.available_duration


        overlapping_slots = []
        for date, user1_slots in user1_date_to_slots.items():
            user2_slots = user2_date_to_slots.get(date)
            if user2_slots:
                for slot_num, user1_slot_duration in enumerate(user1_slots):
                    user2_slot_duration = user2_slots[slot_num]
                    if user1_slot_duration and user2_slot_duration:
                        overlapping_slots.append({
                            "date": date,
                            "slot": slot_num,
                            "available_duration": min(user1_slot_duration, user2_slot_duration),
                        })

        return overlapping_slots