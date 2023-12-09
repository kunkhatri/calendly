from calendly.repositories import CalendlyRepository
from calendly.entities.user import User
from calendly.entities.datetime import Weekday
import os
from typing import Optional
import json
from calendly.utils.datetime import read_data_from_file, overwrite_data_to_file
from calendly.misc.constants import DATE_TIME_FORMAT
from datetime import datetime
from math import floor

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

    def add(self, entity: User) -> User:
        file_content = read_data_from_file(self.path_to_data_dir)
        objs = json.loads(file_content)
        self._pre_process_before_add(entity)
        objs.append(entity.to_dict())
        overwrite_data_to_file(self.path_to_data_dir, json.dumps(objs))
        return entity

    def add_in_bulk(self, entities: list[User]):
        pass

    @classmethod
    def to_entity(cls, obj) -> User:
        created_at = None if not obj.get("created_at") or obj.get("created_at") == "None" else datetime.strptime(obj["created_at"], DATE_TIME_FORMAT)
        updated_at = None if not obj.get("updated_at") or obj.get("updated_at") == "None" else datetime.strptime(obj["updated_at"], DATE_TIME_FORMAT)
        return User(
            id=obj.get("id"),
            created_at=created_at,
            updated_at=updated_at,
            created_by=obj.get("created_by"),
            last_updated_by=obj.get("last_updated_by"),
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

    @classmethod
    def _pre_process_before_add(cls, entity: User):
        super(UserRepository, cls)._pre_process_before_add(entity)
        entity.id = "user" + str(floor(datetime.timestamp(datetime.utcnow())))