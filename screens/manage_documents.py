from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.button import MDRaisedButton, MDIconButton, MDTextButton
from kivymd.uix.snackbar import MDSnackbar
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.list import MDList, OneLineAvatarIconListItem, IconRightWidget

import plyer
import os
import sys
import re
import subprocess
import shutil
from functools import partial

from store.current_client import CurrentClientStore


class ManageDocumentsScreen:
    root = None
    before_slash_regex = (
        re.compile(r"(?<=\\)[^\\]+$")
        if sys.platform == "win32"
        else re.compile(r"/([^/]+)$")
    )
    file_list = None

    def init(self, root):
        self.root = root

    def init_files(self):
        client_dir = os.path.expanduser(
            f"~/.pcc/{CurrentClientStore.current_client.fullname}"
        )
        if not os.path.isdir(client_dir):
            os.makedirs(client_dir)

    def build(self) -> MDScreen:
        self.file_list = MDList(id="file_list")
        return MDScreen(
            MDBoxLayout(
                MDBoxLayout(
                    MDIconButton(icon="arrow-left", on_press=self.go_back),
                    MDLabel(text="Client Documents", font_style="H3"),
                    MDTextButton(
                        text="Open Documents",
                        on_press=self.open_file_explorer,
                        pos_hint={"top": 0.6, "right": 0.5},
                        padding_x=0.5,
                    ),
                    MDRaisedButton(text="Add Document", on_press=self.open_file_upload),
                    adaptive_height=True,
                    spacing="12dp",
                    id="app_bar",
                ),
                MDScrollView(self.file_list, id="file_list_box"),
                padding=[12, 10],
                pos_hint={"top": 1},
                spacing="12dp",
                orientation="vertical",
                id="manage_documents_screen_box",
            ),
            name="manage_documents",
        )

    def refresh(self):
        self.file_list.clear_widgets()

        files = os.listdir(
            os.path.expanduser(f"~/.pcc/{CurrentClientStore.current_client.fullname}")
        )

        for file in files:
            self.file_list.add_widget(
                OneLineAvatarIconListItem(IconRightWidget(icon="trash-can", on_press=partial(self.delete_doc, file)), text=file)
            )

    def open_file_upload(self, _):
        chooser = plyer.filechooser
        files = chooser.open_file()

        if len(files) == 0:
            return

        filename = self.before_slash_regex.findall(files[0])[0]

        # copy selected file to client directory
        shutil.copyfile(
            files[0],
            os.path.expanduser(
                f"~/.pcc/{CurrentClientStore.current_client.fullname}/{filename}"
            ),
        )

        self.refresh()

        MDSnackbar(
            MDLabel(text=f"Successfully added {filename} to documents!"),
            size_hint_x=0.7,
            pos=(dp(12), dp(12)),
        ).open()

    def open_file_explorer(self, _):
        client_path = os.path.expanduser(
            f"~/.pcc/{CurrentClientStore.current_client.fullname}"
        )
        if sys.platform == "win32":
            os.startfile(client_path)

        elif sys.platform == "darwin":
            subprocess.Popen(["open", client_path])

        else:
            try:
                subprocess.Popen(["xdg-open", client_path])
            except OSError:
                # err, think of something else to try
                # xdg-open *should* be supported by recent Gnome, KDE, Xfce
                # for now just pass as windows is main platform anyway
                pass

    def delete_doc(self, file, _):
        os.remove(os.path.expanduser(f"~/.pcc/{CurrentClientStore.current_client.fullname}/{file}"))

        self.refresh()

    def go_back(self, _):
        root_box = self.root.ids.root_box
        screen_manager_content = root_box.ids.screen_manager_content
        screen_manager_content.current = "documents"
