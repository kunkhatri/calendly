from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime
from abc import ABC
from typing import Optional

@dataclass
class CalendlyEntity(ABC):
    id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    created_by: Optional[str]
    last_updated_by: Optional[str]

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "created_at": str(self.created_at),
            "updated_at": str(self.updated_at),
            "created_by": self.created_by,
            "last_updated_by": self.last_updated_by,
        }
