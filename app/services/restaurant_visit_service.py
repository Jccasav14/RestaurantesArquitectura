from app.extensions import redis_client
from app.models.db import Restaurant

class RestaurantVisitService:

    #Registra una visita de un usuario a un restaurante específico
    @staticmethod
    def register_visit(user_id, restaurant_id):
        key = f"user:{user_id}:restaurant_visits"
        redis_client.hincrby(key, restaurant_id, 1)

    #Obtiene las estadísticas de visitas de un usuario a diferentes restaurantes
    @staticmethod
    def get_visit_stats(user_id):
        key = f"user:{user_id}:restaurant_visits"
        data = redis_client.hgetall(key)    # Trae todos los campos del hash
        stats = {}
        # Por cada restaurant_id almacenado, consulta su nombre en la base de datos
        for rest_id, count in data.items():
            restaurant = Restaurant.query.get(int(rest_id))
            if restaurant:
                stats[restaurant.name] = int(count) # Almacena en el resultado final
        return stats
