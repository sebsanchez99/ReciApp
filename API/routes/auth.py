import json
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, create_access_token
from datetime import timedelta
from config import get_db_connection

auth_bp=Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['POST'])
def login():
    conn=get_db_connection()
    cursor=conn.cursor(dictionary=True)
    try:
        data=request.json
        email=data.get("email")
        contraseña=data.get("contraseña")
        if not email or not contraseña:
            return jsonify({"error": "Faltan datos obligatorios"}), 400
      
        cursor.callproc("sp_obtener_usuario_por_email", (email,))
        usuario=None
        for result in cursor.stored_results():
            usuario=result.fretchone()
            break
        if usuario and usuario["contraseña"]==contraseña:
         
            access_token=create_access_token(
                identity=json.dumps({"id": usuario["id"], "email": usuario["email"], "rol_id": usuario["rol_id"]}),
                expires_delta=timedelta(hours=2)
            )
            return jsonify({"mensaje": "Inicio de sesion exitoso", "token": access_token}),
        else:
            return jsonify({"error": "Credenciales incorrectas"}), 401
    except Exception as e:
       return jsonify({"error": str(e)}), 500
    finally:
       cursor.close()
       conn.close()
       
        
