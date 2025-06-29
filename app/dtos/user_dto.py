#DTO del usuario
class UserDTO:
    def __init__(self, id, username, email, role):
        self.id = id          # Identificador único del usuario
        self.username = username  # Nombre de usuario
        self.email = email        # Correo electrónico
        self.role = role          # Rol del usuario (admin, customer, etc.)

