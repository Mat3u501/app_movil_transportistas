from kivy.uix.screenmanager import Screen
import requests

class LoginScreen(Screen):
    def login(self):
        email = self.ids.email_input.text  # Obtener el email del campo de texto
        password = self.ids.password_input.text  # Obtener la contraseña del campo de texto

        # Enviar los datos al backend para la autenticación
        response = requests.post("http://127.0.0.1:5000/auth/login", json={"email": email, "password": password})

        if response.status_code == 200:
            # Si la respuesta es exitosa, cambia a la pantalla de Dashboard
            self.manager.current = "dashboard"
        else:
            # Si el login falla, muestra un mensaje de error
            self.ids.error_label.text = "Email o contraseña incorrectos"
