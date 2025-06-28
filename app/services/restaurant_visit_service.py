from app.extensions import redis_client
from app.models.db import Restaurant

class RestaurantVisitService:
    @staticmethod
    def register_visit(user_id, restaurant_id):
        key = f"user:{user_id}:restaurant_visits"
        redis_client.hincrby(key, restaurant_id, 1)

    @staticmethod
    def get_visit_stats(user_id):
        key = f"user:{user_id}:restaurant_visits"
        data = redis_client.hgetall(key)
        stats = {}
        for rest_id, count in data.items():
            restaurant = Restaurant.query.get(int(rest_id))
            if restaurant:
                stats[restaurant.name] = int(count)
        return stats
