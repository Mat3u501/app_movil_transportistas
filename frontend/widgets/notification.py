from kivy.uix.screenmanager import Screen
from kivy.lang import Builder

Builder.load_string("""
<Notification>:
    BoxLayout:
        orientation: 'vertical'
        Label:
            text: 'Notificaciones'
            font_size: '20sp'
        Button:
            text: 'Volver al Dashboard'
            on_release: app.root.current = 'dashboard'
""")

class Notification(Screen):
    pass
