from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel


class MailScreen:

    def build(self):
        return MDScreen(
            MDBoxLayout(
                MDLabel(
                    text="Hello from mails"
                ),
                padding=[12, 0]
            ),
            name="mail",
        )