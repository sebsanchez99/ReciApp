from flask import Flask
from flask_jwt_extended import JWTManager
from routes.users import users_bp
from routes.auth import auth_bp
from routes.material import material_bp

app = Flask(__name__)

# Configuración de JWT
app.config['JWT_SECRET_KEY'] = 'secreto'
jwt = JWTManager(app)

# Registro de Blueprints
app.register_blueprint(users_bp, url_prefix='/user')
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(material_bp, url_prefix='/material')

if __name__ == '__main__':
    app.run(debug=True)