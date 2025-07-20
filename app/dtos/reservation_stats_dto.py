#DTO de las estadisticas de las reservas
class ReservationStatsDTO:
    def __init__(self, date, total):
        self.date = date    #Fechas
        self.total = total  #Total

    ## Convierte el objeto a diccionario (útil para JSON)
    def to_dict(self):
        return {
            "date": self.date,
            "total": self.total
        }