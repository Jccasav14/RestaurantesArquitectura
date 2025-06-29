#DTO de las reservaciones
class ReservationDTO:
    def __init__(self, id, customer_id, restaurant_id, table_id, reservation_date, reservation_time, special_requests, menu=None,
                 customer=None, restaurant=None, table=None):
        self.id = id                          # ID único de la reservación
        self.customer_id = customer_id        # ID del cliente que reservó
        self.restaurant_id = restaurant_id    # ID del restaurante
        self.table_id = table_id              # ID de la mesa reservada
        self.reservation_date = reservation_date  # Fecha de la reserva
        self.reservation_time = reservation_time  # Hora de la reserva
        self.special_requests = special_requests  # Solicitudes especiales del cliente
        self.menu = menu                      # Platos del menú seleccionados (opcional)
        self.menu = menu

        # Relacionados
        self.customer = customer
        self.restaurant = restaurant
        self.table = table

    #Convierte el DTO a diccionario para facilitar su uso en JSON
    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "restaurant_id": self.restaurant_id,
            "table_id": self.table_id,
            "reservation_date": self.reservation_date.isoformat(),
            "reservation_time": self.reservation_time.strftime('%H:%M'),
            "special_requests": self.special_requests,
            "menu": self.menu
        }
