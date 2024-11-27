from kivy.uix.screenmanager import Screen
import requests

class ProfileScreen(Screen):
    def cargar_historial(self):
        # Obtener el historial de reservas del usuario
        response = requests.get("http://127.0.0.1:5000/mi_historial")

        if response.status_code == 200:
            historial = response.json()
            self.ids.historial_container.clear_widgets()  # Limpiar el historial anterior

            # Mostrar el historial de reservas
            for reserva in historial:
                label = Label(text=f"Reserva: {reserva['turno']} - {reserva['fecha']}")
                self.ids.historial_container.add_widget(label)

    def actualizar_perfil(self):
        
        email = self.ids.email_input.text
        telefono = self.ids.telefono_input.text
        response = requests.put("http://127.0.0.1:5000/actualizar_perfil", json={"email": email, "telefono": telefono})

        if response.status_code == 200:
            self.ids.confirmacion_label.text = "Perfil actualizado correctamente"
        else:
            self.ids.confirmacion_label.text = "Error al actualizar el perfil"
