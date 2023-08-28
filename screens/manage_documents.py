from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton

import plyer

class ManageDocumentsScreen:
    root = None

    def init(self, root):
        self.root = root

    def build(self):
        return MDScreen(
            MDBoxLayout(
                MDLabel(text="Manage Documents", font_style="H3"),
                MDRaisedButton(text="Upload file", on_press=self.open_file_upload),
                padding=[12, 10],
                pos_hint={"top": 1},
                spacing="12dp",
                orientation="vertical",
                id="relations_screen_box",
            ),
            name="manage_documents",
        )

    def open_file_upload(self, _):
        chooser = plyer.filechooser
        filename = chooser.open_file()
        print(filename)