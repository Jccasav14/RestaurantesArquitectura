#DTO de mesas
class TableDTO:
    def __init__(self, id, number, type, capacity, description, restaurant_id):
        self.id = id                  # ID único de la mesa
        self.number = number          # Número identificador de la mesa
        self.type = type              # Tipo de mesa (e.g., interior, exterior)
        self.capacity = capacity      # Capacidad de personas que soporta
        self.description = description # Descripción adicional de la mesa
        self.restaurant_id = restaurant_id  # ID del restaurante al que pertenece

    # Convierte el objeto a diccionario para facilitar su uso en JSON
    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'type': self.type,
            'capacity': self.capacity,
            'description': self.description,
            'restaurant_id': self.restaurant_id,
        }