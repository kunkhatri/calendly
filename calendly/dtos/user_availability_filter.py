from __future__ import annotations

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from datetime import date, datetime, timedelta
from pytz import BaseTzInfo
import calendar
from calendly.misc.constants import DATE_FORMAT

class FilterByNameValues(Enum):
    TODAY = 1
    TOMORROW = 2
    CURRENT_WEEK = 3
    NEXT_WEEK = 4
    CURRENT_MONTH = 5
    NEXT_MONTH = 6

class AvailabilityFilterTypes(Enum):
    NAME = 1
    RANGE = 2

@dataclass
class UserAvailabilityFilter(ABC):
    type: AvailabilityFilterTypes

    @classmethod
    def to_object(cls, filter_dict: dict) -> UserAvailabilityFilter:
        if filter_dict["type"] == AvailabilityFilterTypes.NAME.name:
            return UserAvailabilityFilterByName.to_object(filter_dict)
        elif filter_dict["type"] == AvailabilityFilterTypes.RANGE.name:
            return UserAvailabilityFilterByRange.to_object(filter_dict)
        else:
            raise ValueError(f"Invalid filter type {filter_dict['type']}.")

    @abstractmethod
    def get_date_range(self, timezone: str) -> tuple[date, date]:
        pass

@dataclass
class UserAvailabilityFilterByName(UserAvailabilityFilter):
    value: FilterByNameValues

    @classmethod
    def to_object(cls, filter_dict: dict) -> UserAvailabilityFilter:
        return UserAvailabilityFilterByName(filter_dict["type"], FilterByNameValues[filter_dict["value"]])

    def get_date_range(self, tz: BaseTzInfo) -> tuple[date, date]:
        if self.value == FilterByNameValues.TODAY:
            today = datetime.now(tz).date()
            return (today, today)
        elif self.value == FilterByNameValues.TOMORROW:
            tomorrow = (datetime.now(tz) - timedelta(days=1)).date()
            return (tomorrow, tomorrow)
        elif self.value == FilterByNameValues.CURRENT_WEEK:
            start_date = datetime.now(tz).date()
            end_date = (datetime.now(tz) + timedelta(days=(7 - start_date.weekday() - 1))).date()
            return (start_date, end_date)
        elif self.value == FilterByNameValues.CURRENT_MONTH:
            start_date = datetime.now(tz).date()
            end_date = date(start_date.year, start_date.month, calendar.monthrange(start_date.year, start_date.month)[1])
            return (start_date, end_date)
        elif self.value == FilterByNameValues.NEXT_WEEK:
            now = datetime.now(tz)
            start_date = (now + timedelta(days=(7 - now.weekday()))).date()
            end_date = (now + timedelta(days=(7 - now.weekday())) + timedelta(days=(7 - now.weekday() -1))).date()
            return (start_date, end_date)
        elif self.value == FilterByNameValues.NEXT_MONTH:
            now = datetime.now(tz)
            start_date = (now.replace(day=1) + timedelta(days=32)).replace(day=1)
            end_date = date(start_date.year, start_date.month, calendar.monthrange(start_date.year, start_date.month)[1])
            return (start_date, end_date)
        else:
            raise NotImplementedError(f"Filter by name with value {self.value} not implemented.")

@dataclass
class UserAvailabilityFilterByRange(UserAvailabilityFilter):
    start_date: date
    end_date: date

    @classmethod
    def to_object(cls, filter_dict: dict) -> UserAvailabilityFilter:
        start_date = datetime.strptime(filter_dict["start_date"], DATE_FORMAT).date() if isinstance(filter_dict["start_date"], str) else filter_dict["start_date"]
        end_date = datetime.strptime(filter_dict["end_date"], DATE_FORMAT).date() if isinstance(filter_dict["end_date"], str) else filter_dict["end_date"]
        return UserAvailabilityFilterByName(filter_dict["type"], start_date, end_date)

    def get_date_range(self, timezone: str) -> tuple[date, date]:
        return (self.start_date, self.end_date)
