class RestaurantDTO:
    def __init__(self, id, name, address, phone, description, image_filename):
        self.id = id
        self.name = name
        self.address = address
        self.phone = phone
        self.description = description
        self.image_filename = image_filename

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'description': self.description,
            'image_filename': self.image_filename
        }
