from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
import requests


class LoginScreen(Screen):
    def login(self):
        email = self.ids.email_input.text
        password = self.ids.password_input.text

        try:
            response = requests.post(
                "http://127.0.0.1:5000/auth/login",
                json={"email": email, "password": password},
            )
            if response.status_code == 200:
                data = response.json()
                self.manager.user_id = data.get("user_id")
                self.manager.current = "dashboard"
            else:
                self.ids.error_label.text = "Email o contraseña incorrectos"
        except Exception as e:
            print(f"Error en el login: {e}")
            self.ids.error_label.text = "Error interno del cliente"

    def go_to_register(self):
        self.manager.current = "register"


class RegisterScreen(Screen):
    def register(self):
        name = self.ids.register_name_input.text
        email = self.ids.register_email_input.text
        password = self.ids.register_password_input.text

        if not all([name, email, password]):
            self.ids.register_error_label.text = "Todos los campos son obligatorios"
            return

        try:
            response = requests.post(
                "http://127.0.0.1:5000/auth/register",
                json={"nombre": name, "email": email, "password": password},
            )
            if response.status_code == 201:
                self.manager.current = "login"
            else:
                self.ids.register_error_label.text = response.json().get(
                    "error", "Error al registrarse, intenta nuevamente."
                )
        except Exception as e:
            print(f"Error en el registro: {e}")
            self.ids.register_error_label.text = "Error interno del cliente"

    def go_to_login(self):
        self.manager.current = "login"


class DashboardScreen(Screen):
    def on_enter(self):
        user_id = self.manager.user_id
        if user_id:
            self.cargar_turnos(user_id)
        else:
            self.ids.dashboard_error_label.text = "Error al obtener la información del usuario"

    def cargar_turnos(self, user_id):
        try:
            print(user_id)
            response = requests.get(f"http://127.0.0.1:5000/turn/listar/{user_id}")
            if response.status_code == 200:
                turnos = response.json()
                self.ids.turnos_container.clear_widgets()

                for turno in turnos:
                    turno_box = BoxLayout(orientation="horizontal", size_hint_y=None, height=40)

                    # Etiqueta del turno
                    turno_label = Label(
                        text=f"Vehículo: {turno['vehiculo']} | Matrícula: {turno['matricula']} | Fecha: {turno['fecha_turno']} | Estado: {turno['estado']}",
                        color=(0, 0, 0, 1)
                    )
                    turno_box.add_widget(turno_label)

                    # Botón para eliminar el turno
                    eliminar_btn = Button(text="Eliminar", size_hint_x=0.2)
                    eliminar_btn.bind(on_release=lambda btn, turno_id=turno["id"]: self.eliminar_turno(turno_id))
                    turno_box.add_widget(eliminar_btn)

                    self.ids.turnos_container.add_widget(turno_box)

            else:
                self.ids.dashboard_error_label.text = "Error al cargar los turnos"
        except Exception as e:
            print(f"Error al cargar turnos: {e}")
            self.ids.dashboard_error_label.text = "Error interno del cliente"

    def eliminar_turno(self, turno_id):
        try:
            response = requests.delete(f"http://127.0.0.1:5000/turn/eliminar/{turno_id}")
            if response.status_code == 200:
                # Recargar la lista de turnos tras eliminar uno
                self.cargar_turnos(self.manager.user_id)
            else:
                print(f"Error al eliminar el turno: {response.text}")
        except Exception as e:
            print(f"Error al eliminar turno: {e}")

    def reservar_turno(self, user_id):
        # Obtener los datos de los campos
        vehiculo = self.ids.vehiculo_input.text
        matricula = self.ids.matricula_input.text
        fecha_turno = self.ids.fecha_turno_input.text

        if not all([vehiculo, matricula, fecha_turno]):
            self.ids.dashboard_error_label.text = "Todos los campos son obligatorios"
            return

        try:
            response = requests.post(
                "http://127.0.0.1:5000/turn/crear",
                json={
                    "user_id": self.manager.user_id,
                    "vehiculo": vehiculo,
                    "matricula": matricula,
                    "fecha_turno": fecha_turno,
                },
            )
            if response.status_code == 201:
                self.ids.dashboard_error_label.text = "Turno creado con éxito"
                self.cargar_turnos(self.manager.user_id)  # Actualizar turnos
            else:
                self.ids.dashboard_error_label.text = response.json().get("error", "Error al crear el turno")
        except Exception as e:
            print(f"Error al crear turno: {e}")
            self.ids.dashboard_error_label.text = "Error interno del cliente"

    def logout(self):
        self.manager.user_id = None
        self.manager.current = "login"


class MyScreenManager(ScreenManager):
    user_id = None


class MyApp(App):
    def build(self):
        sm = MyScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(RegisterScreen(name="register"))
        return sm


if __name__ == "__main__":
    MyApp().run()
