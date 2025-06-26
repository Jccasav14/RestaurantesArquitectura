class TableDTO:
    def __init__(self, id, number, type, capacity, description, restaurant_id):
        self.id = id
        self.number = number
        self.type = type
        self.capacity = capacity
        self.description = description
        self.restaurant_id = restaurant_id

    def to_dict(self):
        return {
            'id': self.id,
            'number': self.number,
            'type': self.type,
            'capacity': self.capacity,
            'description': self.description,
            'restaurant_id': self.restaurant_id,
        }