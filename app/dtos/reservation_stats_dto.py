class ReservationStatsDTO:
    def __init__(self, date, total):
        self.date = date
        self.total = total

    def to_dict(self):
        return {
            "date": self.date,
            "total": self.total
        }