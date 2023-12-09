from calendly.repositories import CalendlyRepository
from calendly.entities.user import User
from calendly.entities.datetime import Weekday
import os
from typing import Optional
import json
from calendly.utils.datetime import read_data_from_file
from calendly.misc.constants import DATE_TIME_FORMAT
from datetime import datetime

class UserRepository(CalendlyRepository):
    path_to_data_dir = os.path.join("calendly", "dummy_db", "users.json")

    def get_by_id(self, id: str) -> Optional[User]:
        file_content = read_data_from_file(self.path_to_data_dir)
        objs = json.loads(file_content)

        matched_obj = None
        for obj in objs:
            if obj["id"] == id:
                matched_obj = obj
                break

        return self.to_entity(matched_obj) if matched_obj else None

    def filter(self, filter_conds: list[dict]) -> User:
        """
        :param filter_conds: list of filter conditions to be ANDed
            [
                {
                    "key": <column_name1>,
                    "value": <column_value1>,
                    "op": <comparison_operator1>,
                },
                {
                    "key": <column_name1>,
                    "value": <column_value2>,
                    "op": <comparison_operator2>,
                },
            ]
        :return:
        """
        pass

    def add(self, entity: User):
        pass

    def add_in_bulk(self, entities: list[User]):
        pass

    @classmethod
    def to_entity(cls, obj) -> User:
        return User(
            id=obj["id"],
            created_at=datetime.strptime(obj["created_at"], DATE_TIME_FORMAT),
            updated_at=datetime.strptime(obj["updated_at"], DATE_TIME_FORMAT),
            created_by=obj["created_by"],
            last_updated_by=obj["last_updated_by"],
            name=obj["name"],
            organization=obj["organization"],
            timezone=obj["timezone"],
            working_days=[Weekday[day] for day in obj["working_days"]]
        )

    def remove(self, entity: User):
        pass

    def update(self, entity: User) -> User:
        pass

    def update_in_bulk(self, entity: User) -> User:
        pass
