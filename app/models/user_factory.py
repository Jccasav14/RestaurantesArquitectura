from abc import ABC, abstractmethod

# Clase abstracta base para definir un tipo de usuario genérico
class User(ABC):
    #Método abstracto que debe devolver el rol del usuario
    @abstractmethod
    def get_role(self):
        pass

#Implementación concreta de un usuario con rol 'customer'
class Customer(User):
    def get_role(self):
        return "customer"

#Implementación concreta de un usuario con rol 'restaurant'
class Restaurant(User):
    def get_role(self):
        return "restaurant"

#Fábrica para crear instancias de usuarios según el tipo
class UserFactory:
    @staticmethod
    def create_user(user_type):
        if user_type == "customer":
            return Customer()
        elif user_type == "restaurant":
            return Restaurant()
        else:
            raise ValueError("Invalid user type")