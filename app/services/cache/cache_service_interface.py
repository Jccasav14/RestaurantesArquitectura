from abc import ABC, abstractmethod

#Interfaz (abstracta) para servicios de caché
class ICacheService(ABC):
    #Recupera un valor de la cache
    @abstractmethod
    def get(self, key): pass

    #Guarda un valor en la cache
    @abstractmethod
    def set(self, key, value, ex=None): pass

    #Elimina un valor de la cache
    @abstractmethod
    def delete(self, key): pass
