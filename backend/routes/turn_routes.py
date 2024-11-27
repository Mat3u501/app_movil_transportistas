from flask import Blueprint, request, jsonify
from database.db_connection import get_db_connection
from datetime import datetime, timedelta

turn_bp = Blueprint('turn', __name__)

@turn_bp.route('/crear', methods=['POST'])
def crear_turno():
    """
    Crea un nuevo turno con las restricciones adecuadas.
    """
    try:
        # Verificar que los datos estén en el cuerpo de la solicitud
        data = request.json
        if not data:
            return jsonify({"error": "No se recibieron datos en la solicitud"}), 400

        # Obtener los datos enviados
        user_id = data.get('user_id')
        vehiculo = data.get('vehiculo')
        matricula = data.get('matricula')
        fecha_turno_str = data.get('fecha_turno')

        # Verificar que todos los campos requeridos estén presentes
        if not all([user_id, vehiculo, matricula, fecha_turno_str]):
            return jsonify({"error": "Faltan campos requeridos"}), 400
        
        # Verificar que la fecha esté en el formato adecuado
        try:
            fecha_turno = datetime.strptime(fecha_turno_str, '%Y-%m-%d %H:%M:%S')
        except ValueError:
            return jsonify({"error": "Formato de fecha inválido, debe ser YYYY-MM-DD HH:MM:SS"}), 400

        # Validar horario permitido
        if not (7 <= fecha_turno.hour < 17):
            return jsonify({"error": "Los turnos solo pueden ser entre las 7:00 AM y las 5:00 PM"}), 400

        # Validar que el turno no coincida con otro (dentro de 10 minutos)
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT COUNT(*) AS count FROM turnos
                WHERE (fecha_turno BETWEEN %s AND %s)
            """, (fecha_turno - timedelta(minutes=10), fecha_turno + timedelta(minutes=10)))
            resultado = cursor.fetchone()

            if resultado and resultado['count'] > 0:
                return jsonify({"error": "Ya existe un turno en este rango de tiempo"}), 400

            # Insertar en la base de datos
            cursor.execute("""
                INSERT INTO turnos (user_id, vehiculo, matricula, fecha_turno, estado)
                VALUES (%s, %s, %s, %s, 'pendiente')
            """, (user_id, vehiculo, matricula, fecha_turno))
            conn.commit()

        return jsonify({"message": "Turno reservado exitosamente"}), 201

    except Exception as e:
        print(f"Error al crear turno: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


@turn_bp.route('/listar/<int:user_id>', methods=['GET'])
def listar_turnos(user_id):
    """
    Lista los turnos de un usuario específico.
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("""
                SELECT id, vehiculo, matricula, fecha_turno, estado
                FROM turnos WHERE user_id = %s ORDER BY fecha_turno DESC
            """, (user_id,))
            turnos = cursor.fetchall()
        return jsonify(turnos), 200

    except Exception as e:
        print(f"Error al listar turnos: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500


@turn_bp.route('/eliminar/<int:turn_id>', methods=['DELETE'])
def eliminar_turno(turn_id):
    """
    Elimina un turno por su ID.
    """
    try:
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute("DELETE FROM turnos WHERE id = %s", (turn_id,))
            conn.commit()
        return jsonify({"message": "Turno eliminado exitosamente"}), 200

    except Exception as e:
        print(f"Error al eliminar turno: {e}")
        return jsonify({"error": "Error interno del servidor"}), 500
