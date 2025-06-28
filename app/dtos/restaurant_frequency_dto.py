class RestaurantFrequencyDTO:
    def __init__(self, name=None, count=0):
        self.name = name if name is not None else ""
        self.count = count if count is not None else 0

    def to_dict(self):
        return {
            "restaurant_name": self.restaurant_name,
            "visit_count": self.visit_count
        }