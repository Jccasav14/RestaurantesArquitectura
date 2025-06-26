class ReservationDTO:
    def __init__(self, id, customer_id, restaurant_id, table_id, reservation_date, reservation_time, special_requests, menu=None,
                 customer=None, restaurant=None, table=None):
        self.id = id
        self.customer_id = customer_id
        self.restaurant_id = restaurant_id
        self.table_id = table_id
        self.reservation_date = reservation_date
        self.reservation_time = reservation_time
        self.special_requests = special_requests
        self.menu = menu

        # Relacionados
        self.customer = customer
        self.restaurant = restaurant
        self.table = table


    def to_dict(self):
        return {
            "id": self.id,
            "customer_id": self.customer_id,
            "restaurant_id": self.restaurant_id,
            "table_id": self.table_id,
            "reservation_date": self.reservation_date.isoformat(),
            "reservation_time": self.reservation_time.strftime('%H:%M'),
            "special_requests": self.special_requests,
            "menu": self.menu  # ✅ incluirlo
        }
