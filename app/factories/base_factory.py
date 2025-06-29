from abc import ABC, abstractmethod

class AbstractFactory(ABC):
    @abstractmethod
    def create_dto_from_model(self, model):
        pass    # Método que deben implementar las fábricas hijas para convertir un modelo a DTO

    @abstractmethod
    def create_model_from_dto(self, dto):
        pass    # Método que deben implementar las fábricas hijas para convertir un DTO a modelo
