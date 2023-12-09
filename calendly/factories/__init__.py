from abc import ABC, abstractmethod

class BaseFactory(ABC):

    @classmethod
    @abstractmethod
    def create(cls, name: str):
        pass

