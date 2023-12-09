from dataclasses import dataclass
from enum import Enum, IntEnum

class Weekday(Enum):
    MONDAY = 1
    TUESDAY = 2
    WEDNESDAY = 3
    THURSDAY = 4
    FRIDAY = 5
    SATURDAY = 6
    SUNDAY = 7


@dataclass
class TimeSlot:
    start_time: int
    end_time: int

    def __post_init__(self):
        if self.start_time < 0 or self.start_time > 23:
            raise TypeError("Start time should be in 0-23 hours range.")
        if self.end_time < 0 or self.end_time > 23:
            raise TypeError("End time should be in 0-23 hours range.")