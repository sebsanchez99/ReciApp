from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from config import get_db_connection

users_bp = Blueprint('users', __name__)

# TODO: DESCOMENTAR LÍNEAS DE VERIFICACIÓN DE TOKEN EN PRODUCCIÓN

# Crea un usuario
@users_bp.route('/createUser', methods=['POST'])
# @jwt_required()
def create_user():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        data = request.json
        if not all(k in data for k in ('nombre', 'email', 'contraseña', 'documento', 'tipo_documento_id', 'rol_id')):
            return jsonify({'error': 'Faltan datos obligatorios'}), 400

        nombre = data['nombre']
        email = data['email']
        contraseña = data['contraseña']
        documento = data['documento']
        tipo_documento_id = data['tipo_documento_id']
        rol_id = data['rol_id']

        cursor.callproc('sp_crear_usuario', (nombre, email, contraseña, documento, tipo_documento_id, rol_id))
        conn.commit()

        return jsonify({'mensaje': 'Usuario creado correctamente'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Lista los usuarios
@users_bp.route('/listUsers', methods=['GET'])
# @jwt_required()
def list_users():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc('sp_listar_usuarios')

        usuarios = []
        for result in cursor.stored_results():
            usuarios = result.fetchall()

        return jsonify(usuarios), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Obtiene datos del usuario usando el ID
@users_bp.route('/getUser', methods=['GET'])
# @jwt_required()
def get_user():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        id = request.args.get('id')
        cursor.callproc('sp_obtener_usuario', (id,))

        usuario = None
        for result in cursor.stored_results():
            usuario = result.fetchone()
            break

        if usuario:
            return jsonify(usuario), 200
        else:
            return jsonify({'mensaje': 'Usuario no encontrado'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Actualiza el usuario
@users_bp.route('/putUser', methods=['PUT'])
# @jwt_required()
def update_user():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        id = request.args.get('id')
        data = request.json
        if not all(k in data for k in ('nombre', 'email', 'rol_id')):
            return jsonify({'error': 'Faltan datos obligatorios'}), 400

        nombre = data['nombre']
        email = data['email']
        rol_id = data['rol_id']

        cursor.callproc('sp_actualizar_usuario', (id, nombre, email, rol_id))
        conn.commit()

        return jsonify({'mensaje': 'Usuario actualizado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Elimina el usuario
@users_bp.route('/deleteUser', methods=['DELETE'])
# @jwt_required()
def delete_user():
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        id = request.args.get('id')
        cursor.callproc('sp_eliminar_usuario', (id,))
        conn.commit()

        return jsonify({'mensaje': 'Usuario eliminado correctamente'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cursor.close()
        conn.close()
