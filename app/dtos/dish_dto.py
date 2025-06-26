class DishDTO:
    def __init__(self, id, name, ingredients, description, price, image_filename, restaurant_id):
        self.id = id
        self.name = name
        self.ingredients = ingredients
        self.description = description
        self.price = price
        self.image_filename = image_filename
        self.restaurant_id = restaurant_id

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'ingredients': self.ingredients,
            'description': self.description,
            'price': self.price,
            'image_filename': self.image_filename,
            'restaurant_id': self.restaurant_id
        }
