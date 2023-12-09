from dataclasses import dataclass
from calendly.entities import CalendlyEntity
from calendly.entities.datetime import Weekday

@dataclass
class User(CalendlyEntity):
    name: str
    organization: str
    timezone: str
    working_days: list[Weekday]

    def to_dict(self) -> dict:
        dict_obj = super(User, self).to_dict()
        dict_obj.update({
            "name": self.name,
            "organization": self.organization,
            "timezone": self.timezone,
            "working_days": [day.name for day in self.working_days] if self.working_days is not None else None
        })
        return dict_obj
