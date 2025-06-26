from abc import ABC, abstractmethod

class AbstractFactory(ABC):
    @abstractmethod
    def create_dto_from_model(self, model):
        pass

    @abstractmethod
    def create_model_from_dto(self, dto):
        pass
