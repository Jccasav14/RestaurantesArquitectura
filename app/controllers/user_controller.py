from flask import Blueprint, request, jsonify
from app.models.user_factory import UserFactory

#Crea un Blueprint para las rutas relacionadas con usuarios
user_bp = Blueprint('user', __name__, url_prefix='/api/users')

@user_bp.route('/register', methods=['POST'])
def register():
    #Obtiene los datos JSON enviados en la solicitud
    data = request.get_json()
    #Extrae el tipo de usuario a crear
    user_type = data.get('type')
    
    try:
        #Crea un usuario según el tipo usando el patrón Factory
        user = UserFactory.create_user(user_type)
        #Devuelve un mensaje de éxito indicando el tipo de usuario creado
        return jsonify({"message": f"{user.get_role()} created successfully"}), 201
    except ValueError as e:
        #Si el tipo es inválido, devuelve un error 400 con el mensaje
        return jsonify({"error": str(e)}), 400