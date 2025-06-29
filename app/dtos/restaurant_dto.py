#DTO de resturante
class RestaurantDTO:
    def __init__(self, id, name, address, phone, description, image_filename):
        self.id = id                    #ID unioc del restaurante
        self.name = name                #Nombre del restuarnate
        self.address = address          #Direccion
        self.phone = phone              #Telefono
        self.description = description  #Descripcion
        self.image_filename = image_filename  #Nombre del archivo de imagen

    # Convierte el objeto a diccionario (útil para JSON)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'phone': self.phone,
            'description': self.description,
            'image_filename': self.image_filename
        }
