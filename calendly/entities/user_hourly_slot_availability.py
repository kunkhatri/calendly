from dataclasses import dataclass
from calendly.entities import CalendlyEntity
from datetime import date
from calendly.misc.exceptions import InvalidValueException

@dataclass
class UserHourlySlotAvailability(CalendlyEntity):
    # one to many relationship between user id to id
    user_id: str # partition key
    date: date # sort key
    slot: int # should be between 0 - 22 as it specifies hourly slots in a day
    available_duration: int # >=0 and <= 1, considering 1 hour slot

    def __post_init__(self):
        if self.slot < 0 or self.slot > 22:
            raise InvalidValueException(f"Invalid slot value. Slot can only be between 0-23 hrs.")
        elif self.available_duration < 0 or self.available_duration > 1:
            raise InvalidValueException(
                f"Invalid available duration value for the slot. Available duration has to be between 0 - 1."
            )

    def to_dict(self) -> dict:
        dict_obj = super(UserHourlySlotAvailability, self).to_dict()
        dict_obj.update({
            "user_id": self.user_id,
            "date": str(self.date),
            "slot": self.slot,
            "available_duration": self.available_duration,
        })
        return dict_obj

