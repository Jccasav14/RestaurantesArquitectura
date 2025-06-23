from flask import Blueprint, request, jsonify
from app.models.user_factory import UserFactory

user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    user_type = data.get('type')
    
    try:
        user = UserFactory.create_user(user_type)
        return jsonify({"message": f"{user.get_role()} created successfully"}), 201
    except ValueError as e:
        return jsonify({"error": str(e)}), 400