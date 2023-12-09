from calendly.repositories import CalendlyRepository
from calendly.entities.user_hourly_slot_availability import UserHourlySlotAvailability
from calendly.utils.datetime import read_data_from_file, overwrite_data_to_file
import os
from typing import Optional
import json
from datetime import datetime, date
from calendly.misc.constants import DATE_TIME_FORMAT, DATE_FORMAT
from math import floor


class UserHourlySlotAvailabilityRepository(CalendlyRepository):
    path_to_data_dir = os.path.join("calendly", "dummy_db", "users_slots.json")

    def get_by_id(self, id: str) -> Optional[UserHourlySlotAvailability]:
        file_content = read_data_from_file(self.path_to_data_dir)
        objs = json.loads(file_content)

        matched_obj = None
        for obj in objs:
            if obj["id"] == id:
                matched_obj = obj
                break

        return self.to_entity(matched_obj) if matched_obj else None

    def filter(self, filter_conds: list[dict]) -> list[UserHourlySlotAvailability]:
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
        file_content = read_data_from_file(self.path_to_data_dir)
        objs = json.loads(file_content)

        entities = [self.to_entity(obj) for obj in objs] if objs else []

        # hack: logically, this filtering should be happening at db layer before
        # entities are created. but since we only have dummy db here and
        # performing filtering on raw data gets too convoluted, therefore,
        # moving the filtering logic on entities.
        matched_entities = []
        for entity in entities:
            is_matched = True
            for filter_cond in filter_conds:
                key = filter_cond["key"]
                value = filter_cond["value"]
                op = filter_cond["op"]
                if op == "eq":
                    if getattr(entity, key) == value:
                        is_matched = True
                    else:
                        is_matched = False
                        break
                elif op == "neq":
                    if getattr(entity, key) != value:
                        is_matched = True
                    else:
                        is_matched = False
                        break
                elif op == "gt":
                    if getattr(entity, key) > value:
                        is_matched = True
                    else:
                        is_matched = False
                        break
                elif op == "gte":
                    if getattr(entity, key) >= value:
                        is_matched = True
                    else:
                        is_matched = False
                        break
                elif op == "lt":
                    if getattr(entity, key) < value:
                        is_matched = True
                    else:
                        is_matched = False
                        break
                elif op == "lte":
                    if getattr(entity, key) <= value:
                        is_matched = True
                    else:
                        is_matched = False
                        break
                else:
                    raise NotImplementedError(f"Unsupported operation type {op} for filtering operation.")

                if not is_matched:
                    break

            if is_matched:
                matched_entities.append(entity)

        return matched_entities

    def get_user_slots_in_date_range(
        self, user_id: str, start_date: date, end_date: date
    ) -> list[UserHourlySlotAvailability]:
        filter_conds = [
            {
                "key": "user_id",
                "value": user_id,
                "op": "eq",
            },
            {
                "key": "date",
                "value": start_date,
                "op": "gte",
            },
            {
                "key": "date",
                "value": end_date,
                "op": "lte",
            },
        ]
        return self.filter(filter_conds)

    @classmethod
    def _pre_process_before_add(cls, entity: UserHourlySlotAvailability):
        super(UserHourlySlotAvailabilityRepository, cls)._pre_process_before_add(entity)
        entity.id = entity.user_id + "slot" + str(floor(datetime.timestamp(datetime.utcnow())))

    def add(self, entity: UserHourlySlotAvailability) -> UserHourlySlotAvailability:
        file_content = read_data_from_file(self.path_to_data_dir)
        objs = json.loads(file_content)
        self._pre_process_before_add(entity)
        objs.append(entity.to_dict())

        overwrite_data_to_file(self.path_to_data_dir, json.dumps(objs))
        return entity

    def add_in_bulk(self, entities: list[UserHourlySlotAvailability]):
        file_content = read_data_from_file(self.path_to_data_dir)
        objs = json.loads(file_content)

        for entity in entities:
            self._pre_process_before_add(entity)
            objs.append(entity.to_dict())

        overwrite_data_to_file(self.path_to_data_dir, json.dumps(objs))

    @classmethod
    def to_entity(cls, obj) -> UserHourlySlotAvailability:
        created_at = None if not obj.get("created_at") or obj.get("created_at") == "None" else datetime.strptime(obj["created_at"], DATE_TIME_FORMAT)
        updated_at = None if not obj.get("updated_at") or obj.get("updated_at") == "None" else datetime.strptime(obj["updated_at"], DATE_TIME_FORMAT)
        return UserHourlySlotAvailability(
            id=obj.get("id"),
            created_at=created_at,
            updated_at=updated_at,
            created_by=obj.get("created_by"),
            last_updated_by=obj.get("last_updated_by"),
            user_id=obj["user_id"],
            date=datetime.strptime(obj["date"], DATE_FORMAT).date(),
            slot=obj["slot"],
            available_duration=obj["available_duration"],
        )

    def remove(self, entity: UserHourlySlotAvailability):
        pass

    def update(self, entity: UserHourlySlotAvailability) -> UserHourlySlotAvailability:
        pass

    def update_in_bulk(self, entity: UserHourlySlotAvailability) -> UserHourlySlotAvailability:
        pass
