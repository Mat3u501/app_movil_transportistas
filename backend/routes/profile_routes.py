from flask import Blueprint, request, jsonify
from database.db_connection import get_db_connection

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/historial/<int:user_id>', methods=['GET'])
def historial_turnos(user_id):
    """
    Obtiene el historial de turnos de un usuario.
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT t.id, t.fecha_turno, t.estado, t.vehiculo, t.matricula
                FROM turnos t
                WHERE t.user_id = %s
                ORDER BY t.fecha_turno DESC
            """, (user_id,))
            historial = cursor.fetchall()

        if not historial:
            return jsonify({"message": "No se encontraron turnos para este usuario"}), 404

        return jsonify(historial), 200

    except Exception as e:
        print(f"Error al obtener historial de turnos: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


@profile_bp.route('/actualizar', methods=['PUT'])
def actualizar_perfil():
    """
    Actualiza la información del perfil de usuario.
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        nombre = data.get('nombre')
        email = data.get('email')

        # Validar que los campos requeridos estén presentes
        if not all([user_id, nombre, email]):
            return jsonify({"error": "Faltan campos requeridos"}), 400

        # Verificar formato de correo electrónico
        if not email or "@" not in email:
            return jsonify({"error": "Formato de correo electrónico inválido"}), 400

        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                UPDATE users
                SET nombre = %s, email = %s
                WHERE id = %s
            """, (nombre, email, user_id))
            conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "Usuario no encontrado"}), 404

        return jsonify({"message": "Perfil actualizado correctamente"}), 200

    except Exception as e:
        print(f"Error al actualizar perfil: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
