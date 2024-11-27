from kivy.uix.screenmanager import Screen
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
import requests

class DashboardScreen(Screen):
    def cargar_turnos(self, user_id):
        """
        Carga los turnos del usuario autenticado desde el backend.
        """
        try:
            response = requests.get(f"http://127.0.0.1:5000/turn/listar/{user_id}")
            
            if response.status_code == 200:
                turnos = response.json()  # Lista de turnos del usuario
                self.ids.turnos_container.clear_widgets()  # Limpiar los turnos anteriores

                # Mostrar los turnos del usuario
                for turno in turnos:
                    turno_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)

                    # Descripción del turno
                    turno_label = Label(
                        text=f"Vehículo: {turno['vehiculo']} | Matrícula: {turno['matricula']} | Fecha: {turno['fecha_turno']} | Estado: {turno['estado']}",
                        size_hint_y=None,
                        height=40
                    )
                    turno_box.add_widget(turno_label)

                    # Botón para eliminar turno
                    eliminar_button = Button(
                        text="Eliminar",
                        size_hint_x=0.2
                    )
                    eliminar_button.bind(on_press=lambda btn, turno_id=turno['id']: self.eliminar_turno(turno_id))
                    turno_box.add_widget(eliminar_button)

                    # Agregar el box al contenedor
                    self.ids.turnos_container.add_widget(turno_box)
            else:
                self.ids.turnos_container.clear_widgets()
                self.ids.turnos_container.add_widget(Label(text="Error al cargar los turnos"))

        except Exception as e:
            print(f"Error al cargar turnos: {e}")
            self.ids.turnos_container.clear_widgets()
            self.ids.turnos_container.add_widget(Label(text="Error al cargar los turnos"))

    def reservar_turno(self, user_id):
        """
        Reserva un nuevo turno para el usuario.
        """
        vehiculo = self.ids.vehiculo_input.text
        matricula = self.ids.matricula_input.text
        fecha_turno = self.ids.fecha_turno_input.text

        # Validar datos antes de enviar la solicitud
        if not vehiculo or not matricula or not fecha_turno:
            self.ids.confirmacion_label.text = "Por favor, complete todos los campos"
            return

        try:
            response = requests.post("http://127.0.0.1:5000/turn/crear", json={
                "user_id": user_id,
                "vehiculo": vehiculo,
                "matricula": matricula,
                "fecha_turno": fecha_turno
            })

            if response.status_code == 201:
                self.ids.confirmacion_label.text = "Turno reservado con éxito"
                self.cargar_turnos(user_id)  # Recargar la lista de turnos
            else:
                self.ids.confirmacion_label.text = response.json().get("error", "Error desconocido")

        except Exception as e:
            print(f"Error al reservar turno: {e}")
            self.ids.confirmacion_label.text = "Error interno del cliente"

    def eliminar_turno(self, turn_id):
        """
        Elimina un turno por su ID.
        """
        try:
            response = requests.delete(f"http://127.0.0.1:5000/turn/eliminar/{turn_id}")

            if response.status_code == 200:
                self.ids.confirmacion_label.text = "Turno eliminado con éxito"
                # Recargar turnos del usuario actual (se requiere user_id para ello)
                user_id = self.parent.get_screen('login').user_id  # Obtener user_id desde otra screen
                self.cargar_turnos(user_id)
            else:
                self.ids.confirmacion_label.text = response.json().get("error", "Error desconocido")

        except Exception as e:
            print(f"Error al eliminar turno: {e}")
            self.ids.confirmacion_label.text = "Error interno del cliente"
