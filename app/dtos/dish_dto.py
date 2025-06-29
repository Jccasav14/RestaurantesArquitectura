#DTO de los platos
class DishDTO:
    def __init__(self, id, name, ingredients, description, price, image_filename, restaurant_id):
        self.id = id                      # ID único del plato
        self.name = name                  # Nombre del plato
        self.ingredients = ingredients    # Ingredientes del plato
        self.description = description    # Descripción del plato
        self.price = price                # Precio
        self.image_filename = image_filename  # Nombre del archivo de imagen
        self.restaurant_id = restaurant_id    # ID del restaurante al que pertenece

    # Convierte el DTO a un diccionario para usar en JSON
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
