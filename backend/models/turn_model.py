from database.db_connection import get_db_connection

class TurnModel:
    @staticmethod
    def create_turn(user_id, vehiculo, matricula, fecha_turno):
        """
        Crea un nuevo turno.
        :param user_id: ID del usuario que reserva el turno.
        :param vehiculo: Tipo o modelo de vehículo.
        :param matricula: Matrícula del vehículo.
        :param fecha_turno: Fecha y hora del turno.
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("No se pudo establecer conexión con la base de datos")
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    INSERT INTO turnos (user_id, vehiculo, matricula, fecha_turno, estado)
                    VALUES (%s, %s, %s, %s, 'pendiente')
                """, (user_id, vehiculo, matricula, fecha_turno))
                conn.commit()
        except Exception as e:
            print(f"Error al crear el turno: {e}")
            conn.rollback()
        finally:
            conn.close()

    @staticmethod
    def get_available_turns():
        """
        Obtiene todos los turnos disponibles.
        :return: Lista de turnos disponibles.
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("No se pudo establecer conexión con la base de datos")
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    SELECT * FROM turnos WHERE estado = 'pendiente'
                """)
                return cursor.fetchall()
        except Exception as e:
            print(f"Error al obtener los turnos disponibles: {e}")
            return []
        finally:
            conn.close()

    @staticmethod
    def update_turn(turn_id, estado):
        """
        Actualiza el estado de un turno.
        :param turn_id: ID del turno a actualizar.
        :param estado: Nuevo estado para el turno (e.g., 'confirmado', 'cancelado').
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("No se pudo establecer conexión con la base de datos")
        try:
            with conn.cursor() as cursor:
                cursor.execute("""
                    UPDATE turnos SET estado = %s WHERE id = %s
                """, (estado, turn_id))
                conn.commit()
        except Exception as e:
            print(f"Error al actualizar el turno: {e}")
            conn.rollback()
        finally:
            conn.close()

    @staticmethod
    def delete_turn(turn_id):
        """
        Elimina un turno por su ID.
        :param turn_id: ID del turno a eliminar.
        """
        conn = get_db_connection()
        if not conn:
            raise Exception("No se pudo establecer conexión con la base de datos")
        try:
            with conn.cursor() as cursor:
                cursor.execute("DELETE FROM turnos WHERE id = %s", (turn_id,))
                conn.commit()
        except Exception as e:
            print(f"Error al eliminar el turno: {e}")
            conn.rollback()
        finally:
            conn.close()
