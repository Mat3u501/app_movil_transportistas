from kivy.uix.screenmanager import Screen
import requests

class RegisterScreen(Screen):
    def registrar_usuario(self):
        email = self.ids.email_input.text
        password = self.ids.password_input.text
        nombre = self.ids.nombre_input.text
        #vehiculo = self.ids.vehiculo_input.text
        #matricula = self.ids.matricula_input.text

        # Enviar la solicitud al backend para registrar al usuario
        response = requests.post("http://127.0.0.1:5000/auth/registrar", json={
            "email": email,
            "password": password,
            "name": nombre
            #"vehiculo": vehiculo,
            #"matricula": matricula
        })

        if response.status_code == 201:
            # Si la respuesta es exitosa, cambia a la pantalla de login
            self.manager.current = "login"
        else:
            # Si hay algún error, muestra un mensaje
            self.ids.error_label.text = "Error al registrar el usuario"
