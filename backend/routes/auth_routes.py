from flask import Blueprint, request, jsonify
#from werkzeug.security import generate_password_hash, check_password_hash
from database.db_connection import get_db_connection
from models.user_model import UserModel  # Asumiendo que tienes UserModel

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """
    Registra un nuevo usuario.
    Recibe JSON con las claves: nombre, email, password, tipo_usuario.
    """
    try:
        # Validar que el cuerpo de la solicitud tiene los datos requeridos
        data = request.json
        #required_fields = ['name', 'email', 'password', 'tipo_usuario']
        required_fields = ['nombre', 'email', 'password']
        if not all(field in data for field in required_fields):
            print(data)
            return jsonify({"error": "Faltan campos requeridos"}), 400

        nombre = data.get('nombre')
        email = data.get('email')
        password = data.get('password')
        #tipo_usuario = data.get('tipo_usuario')
        print(data)
        print(nombre)
        print(email)
        print(password)

        # Verificar formato de correo y contraseña (opcional)
        if not email or not "@" in email:
            return jsonify({"error": "Formato de correo electrónico inválido"}), 400
        
        if len(password) < 6:            
            return jsonify({"error": "La contraseña debe tener al menos 6 caracteres"}), 400

        # Hashear la contraseña
        #hashed_password = generate_password_hash(password)

        # Conexión a la base de datos y creación del usuario
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                INSERT INTO users (nombre, email, password, tipo_usuario) 
                VALUES (%s, %s, %s, %s)
            """, (nombre, email, password, 'transportista'))
            conn.commit()

        return jsonify({"message": "Usuario registrado exitosamente"}), 201

    except Exception as e:
        print(f"Error al registrar usuario: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """
    Inicia sesión de un usuario.
    Recibe JSON con las claves: email y password.
    """
    try:
        # Validar que el cuerpo de la solicitud tiene los datos requeridos
        data = request.json
        if not all(field in data for field in ['email', 'password']):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        email = data.get('email')
        password = data.get('password')

        # Verificar que el correo electrónico exista en la base de datos
        user = UserModel.get_user_by_email(email)

        #if user and UserModel.verify_password(user['password'], password):
        if email == user['email'] and password == user['password']:
            # Si el usuario existe y la contraseña es correcta
            return jsonify({"message": "Login exitoso", "user_id": user['id']}), 200
        else:
            print(data)
            print("espacio")
            print(user)
            print(password)
            # Si el email o la contraseña son incorrectos
            return jsonify({"error": "Email o contraseña incorrectos"}), 401

    except Exception as e:
        print(f"Error al iniciar sesión: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
