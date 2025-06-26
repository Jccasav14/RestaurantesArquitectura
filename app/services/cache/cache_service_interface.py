from abc import ABC, abstractmethod

class ICacheService(ABC):
    @abstractmethod
    def get(self, key): pass

    @abstractmethod
    def set(self, key, value, ex=None): pass

    @abstractmethod
    def delete(self, key): pass
