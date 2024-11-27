from flask import Flask
from flask_cors import CORS
from routes.auth_routes import auth_bp
from routes.turn_routes import turn_bp
from routes.profile_routes import profile_bp
#from database.db_connection import init_db

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretKey2024'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'transportistas_app'

# Habilitar CORS
CORS(app)

# Inicializar la conexión a la base de datos
#init_db()

# Registrar Blueprints (rutas)
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(turn_bp, url_prefix='/turn')
app.register_blueprint(profile_bp, url_prefix='/profile')

if __name__ == '__main__':
    app.run(debug=True)
