import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_jwt_extended import create_access_token
from config import get_db_connection
from datetime import timedelta

# TODO: DESCOMENTAR LÍNEAS DE VERIFICACIÓN DE TOKEN EN PRODUCCIÓN

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        data = request.json
        email = data.get("email")
        contraseña = data.get("contraseña")

        if not email or not contraseña:
            return jsonify({"error": "Faltan datos obligatorios"}), 400

        cursor.callproc("sp_obtener_usuario_por_email", (email,))
        
        usuario = None
        for result in cursor.stored_results():
            usuario = result.fetchone()
            break

        if usuario and usuario["contraseña"] == contraseña:
            # Genera token 
            access_token = create_access_token(
                identity=json.dumps({"id": usuario["id"], "email": usuario["email"], "rol_id": usuario["rol_id"]}),
                expires_delta=timedelta(hours=2)
            )
            return jsonify({"mensaje": "Inicio de sesión exitoso", "token": access_token}), 200
        else:
            return jsonify({"error": "Credenciales incorrectas"}), 401
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

@auth_bp.route('/changePassword', methods=['PUT'])
@jwt_required()
def change_password():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        data = request.json
        nueva_contraseña = data.get("nueva_contraseña")

        if not nueva_contraseña:
            return jsonify({"error": "La nueva contraseña es obligatoria"}), 400

        # Obtiene el usuario autenticado desde el token
        identidad = json.loads(get_jwt_identity())  
        print(identidad["id"])
        user_id = identidad["id"]

        cursor.callproc("sp_cambiar_contraseña", (user_id, nueva_contraseña))
        conn.commit()

        return jsonify({"mensaje": "Contraseña actualizada exitosamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()