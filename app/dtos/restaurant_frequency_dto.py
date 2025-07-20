#DTO de las veces qeun cliente ha visitado un restaurante especifico
class RestaurantFrequencyDTO:
    def __init__(self, name=None, count=0):
        self.name = name if name is not None else ""    #Nombre del restuarante
        self.count = count if count is not None else 0  #Numero de visitas

    #Convierte el objeto a diccionario para facilitar su uso en JSON
    def to_dict(self):
        return {
            "restaurant_name": self.restaurant_name,
            "visit_count": self.visit_count
        }