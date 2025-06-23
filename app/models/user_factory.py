from abc import ABC, abstractmethod

class User(ABC):
    @abstractmethod
    def get_role(self):
        pass

class Customer(User):
    def get_role(self):
        return "customer"

class Restaurant(User):
    def get_role(self):
        return "restaurant"

class UserFactory:
    @staticmethod
    def create_user(user_type):
        if user_type == "customer":
            return Customer()
        elif user_type == "restaurant":
            return Restaurant()
        else:
            raise ValueError("Invalid user type")