from __future__ import annotations

from dataclasses import dataclass
from abc import ABC
from enum import Enum
import datetime
from calendly.misc.constants import DATE_FORMAT

class AvailabilityConfigTypes(Enum):
    PER_DATE = 1
    PATTERN = 2

@dataclass()
class DateSlots:
    date: datetime.date
    slots: list[tuple[int, int]]

    def __post_init__(self):
        for slot in self.slots:
            start, end = slot
            if start < 0 or start > 22 or end < 1 or end > 23:
                raise ValueError(
                    f"Invalid slots provided for date {self.date}. Each slot should be a tuple in range 0-23."
                )

@dataclass
class AvailabilityConfig(ABC):
    type: AvailabilityConfigTypes

    @classmethod
    def to_object(cls, availability_config: dict) -> AvailabilityConfig:
        if availability_config["type"] == AvailabilityConfigTypes.PER_DATE.name:
            return PerDateAvailabilityConfig.to_object(availability_config)
        elif availability_config["type"] == AvailabilityConfigTypes.PATTERN.name:
            return PatternBasedAvailabilityConfig.to_object(availability_config)
        else:
            raise TypeError(f"Invalid availability config {availability_config['type']}.")

@dataclass
class PerDateAvailabilityConfig(AvailabilityConfig):
    dates_slots: list[DateSlots]

    @classmethod
    def to_object(cls, availability_config: dict) -> PerDateAvailabilityConfig:
        return PerDateAvailabilityConfig(
            type=availability_config["type"],
            dates_slots=[DateSlots(date=datetime.datetime.strptime(date_slot["date"], DATE_FORMAT).date(), slots=date_slot["slots"]) for date_slot in availability_config["dates_slots"]]
        )

@dataclass
class PatternBasedAvailabilityConfig(AvailabilityConfig):
    date_slots: DateSlots
    # should be cron like pattern but with only three parameters
    # * * *:
    #   first * -> day of the month
    #   second * -> month
    #   third * -> day of the week
    repetition_pattern: str

    @classmethod
    def to_object(cls, availability_config: dict) -> PatternBasedAvailabilityConfig:
        return PatternBasedAvailabilityConfig(
            type=availability_config["type"],
            date_slots=DateSlots(date=datetime.datetime.strptime(availability_config["date_slots"]["date"], DATE_FORMAT).date(), slots=availability_config["date_slots"]["slots"]),
            repetition_pattern=availability_config["repetition_pattern"],
        )
