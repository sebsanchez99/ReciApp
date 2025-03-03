from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from config import get_db_connection

material_bp = Blueprint('material', __name__)

# TODO: DESCOMENTAR LÍNEAS DE VERIFICACIÓN DE TOKEN EN PRODUCCIÓN

# Crear el material
@material_bp.route('/createMaterial', methods=['POST'])
# @jwt_required()
def crear_material():
    data = request.json
    nombre = data.get('nombre')
    precio_por_kg = data.get('precio_por_kg')

    if not nombre or not precio_por_kg:
        return jsonify({"error": "Faltan datos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc('sp_crear_material', (nombre, precio_por_kg))
        conn.commit()
        return jsonify({"mensaje": "Material creado correctamente"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Lista materiales
@material_bp.route('/listMaterials', methods=['GET'])
# @jwt_required()
def listar_materiales():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc('sp_listar_materiales')
        
        materiales = []
        for result in cursor.stored_results():
            materiales = result.fetchall()
            break

        return jsonify(materiales), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Obtiene el material por ID
@material_bp.route('/getMaterial', methods=['GET'])
# @jwt_required()
def obtener_material():
    id = request.args.get('id')

    if not id:
        return jsonify({"error": "Falta el parámetro 'id'"}), 400

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.callproc('sp_obtener_material', (id,))
        
        material = None
        for result in cursor.stored_results():
            material = result.fetchone()
            break

        if material:
            return jsonify(material), 200
        return jsonify({"mensaje": "Material no encontrado"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Actualiza el material
@material_bp.route('/updateMaterial', methods=['PUT'])
# @jwt_required()
def actualizar_material():
    id = request.args.get('id')
    data = request.json
    nombre = data.get('nombre')
    precio_por_kg = data.get('precio_por_kg')

    if not id or not nombre or not precio_por_kg:
        return jsonify({"error": "Faltan datos"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc('sp_actualizar_material', (id, nombre, precio_por_kg))
        conn.commit()
        return jsonify({"mensaje": "Material actualizado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# Elimina el material
@material_bp.route('/deleteMaterial', methods=['DELETE'])
# @jwt_required()
def eliminar_material():
    id = request.args.get('id')

    if not id:
        return jsonify({"error": "Falta el parámetro 'id'"}), 400

    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.callproc('sp_eliminar_material', (id,))
        conn.commit()
        return jsonify({"mensaje": "Material eliminado correctamente"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cursor.close()
        conn.close()