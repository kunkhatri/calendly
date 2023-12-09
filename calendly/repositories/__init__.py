from abc import ABC, abstractmethod
from calendly.entities import CalendlyEntity
from typing import Optional

class CalendlyRepository(ABC):
    path_to_data_dir = None

    def __init__(self):
        self.db_session = None


    @abstractmethod
    def get_by_id(self, id: str) -> Optional[CalendlyEntity]:
        pass

    def __getitem__(self, id: str) -> Optional[CalendlyEntity]:
        return self.get_by_id(id)

    @abstractmethod
    def filter(self, filter_conds: list[dict]) -> CalendlyEntity:
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

    @abstractmethod
    def add(self, entity: CalendlyEntity):
        pass

    @abstractmethod
    def add_in_bulk(self, entities: list[CalendlyEntity]):
        pass

    @abstractmethod
    def remove(self, entity: CalendlyEntity):
        pass

    @abstractmethod
    def update(self, entity: CalendlyEntity) -> CalendlyEntity:
        pass

    @abstractmethod
    def update_in_bulk(self, entity: CalendlyEntity) -> CalendlyEntity:
        pass
