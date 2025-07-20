# app/controllers/chat_controller.py

from flask import Blueprint, request, jsonify, current_app
from flask_login import login_required, current_user
import os, requests
from requests.exceptions import RequestException
from app.models.db import Restaurant, Category, Dish

chat_bp = Blueprint('chat', __name__)

# Configuración de modelos disponibles
MODEL_CONFIG = {
    "llama3-8b": {
        "model": "llama3-8b-8192",
        "max_tokens": 4096,
        "temperature": 0.6,
        "timeout": 30
    },
    "mixtral-8x7b": {
        "model": "mixtral-8x7b-32768",
        "max_tokens": 8192,
        "temperature": 0.7,
        "timeout": 45
    },
    "llama3-70b": {
        "model": "llama3-70b-8192",
        "max_tokens": 4096,
        "temperature": 0.6,
        "timeout": 60
    }
}

def build_system_context():
    """Construye el contexto del sistema basado en la base de datos"""
    restos = [r.name for r in Restaurant.query.all()]
    cats = [c.name for c in Category.query.all()]
    platos = [d.name for d in Dish.query.all()]

    return (
        "Eres un asistente especializado en restaurantes. "
        "Datos disponibles:\n"
        f"- Restaurantes: {', '.join(restos) if restos else 'Ninguno registrado'}\n"
        f"- Categorías: {', '.join(cats) if cats else 'Ninguna disponible'}\n"
        f"- Platos: {', '.join(platos) if platos else 'Ninguno en el menú'}\n"
        "Responde de forma concisa y profesional."
    )

@chat_bp.route('/chatbot', methods=['POST'])
@login_required
def chatbot():
    # 1. Validación inicial
    if not request.is_json:
        return jsonify({'error': 'Se requiere contenido tipo JSON'}), 400

    user_message = request.json.get('message', '').strip()
    if not user_message:
        return jsonify({'error': 'El mensaje no puede estar vacío'}), 400

    # 2. Configuración del modelo
    model_name = request.json.get('model', 'llama3-8b')  # Default a Llama3 8B
    if model_name not in MODEL_CONFIG:
        model_name = 'llama3-8b'
    
    config = MODEL_CONFIG[model_name]
    current_app.logger.info(f"Usando modelo: {model_name}")

    try:
        # 3. Construir contexto
        system_ctx = build_system_context()

        # 4. Preparar payload para Groq API
        payload = {
            "model": config["model"],
            "messages": [
                {"role": "system", "content": system_ctx},
                {"role": "user", "content": user_message}
            ],
            "temperature": config["temperature"],
            "max_tokens": config["max_tokens"]
        }

        # 5. Verificar API key
        api_key = os.getenv('GROQ_API_KEY')
        if not api_key:
            current_app.logger.error("Falta la API key de Groq")
            return jsonify({'error': 'Error de configuración del servidor'}), 500

        # 6. Hacer la petición
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=config["timeout"]
        )

        # 7. Procesar respuesta
        response.raise_for_status()
        response_data = response.json()

        if not response_data.get('choices'):
            raise ValueError("Respuesta inesperada de la API")

        answer = response_data['choices'][0]['message']['content']
        return jsonify({
            'response': answer.strip(),
            'model_used': model_name
        })

    except RequestException as e:
        current_app.logger.error(f"Error de conexión: {str(e)}")
        # Reintentar con modelo más ligero si falla
        if model_name != 'llama3-8b':
            current_app.logger.info("Reintentando con llama3-8b...")
            request.json['model'] = 'llama3-8b'
            return chatbot()
        return jsonify({'error': 'No se pudo conectar con el servicio de chat'}), 503

    except Exception as e:
        current_app.logger.error(f"Error inesperado: {str(e)}")
        return jsonify({'error': 'Error procesando tu solicitud'}), 500