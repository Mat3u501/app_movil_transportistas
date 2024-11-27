from database.db_connection import get_db_connection
from werkzeug.security import check_password_hash

class UserModel:
    @staticmethod
    def get_user_by_email(email):
        """
        Obtiene un usuario por su correo electrónico.
        :param email: Correo electrónico del usuario.
        :return: Diccionario con los datos del usuario o None si no existe.
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("No se pudo establecer conexión con la base de datos")
        try:
            with conn.cursor() as cursor:
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()
            return user
        except Exception as e:
            print(f"Error al obtener el usuario por correo: {e}")
            return None
        finally:
            conn.close()

    @staticmethod
    def create_user(nombre, email, password, tipo_usuario):
        """
        Crea un nuevo usuario.
        :param nombre: Nombre completo del usuario.
        :param email: Correo electrónico del usuario.
        :param password: Contraseña cifrada del usuario.
        :param tipo_usuario: Tipo de usuario (e.g., 'admin', 'cliente').
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("No se pudo establecer conexión con la base de datos")
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO users (nombre, email, password, tipo_usuario) 
                    VALUES (%s, %s, %s, %s)
                """, (nombre, email, password, tipo_usuario))
                conn.commit()
        except Exception as e:
            print(f"Error al crear el usuario: {e}")
            conn.rollback()
        finally:
            conn.close()

    @staticmethod
    def verify_password(stored_password, provided_password):
        """
        Verifica si la contraseña proporcionada coincide con la almacenada.
        :param stored_password: Contraseña cifrada almacenada en la base de datos.
        :param provided_password: Contraseña proporcionada por el usuario.
        :return: True si las contraseñas coinciden, False en caso contrario.
        """
        try:
            return check_password_hash(stored_password, provided_password)
        except Exception as e:
            print(f"Error al verificar la contraseña: {e}")
            return False
