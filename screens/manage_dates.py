from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.button import MDIconButton, MDFloatingActionButton

import objectbox
from models.date import Date
from objectbox_handler import ob

from store.current_date import CurrentDateStore

class ManageDatesScreen:

    root = None
    data_table = None
    events_box = objectbox.Box(ob, Date)
    add_dialog = None

    def init(self, root):
        self.root = root

    def build(self):

        events = self.events_box.get_all()

        events = filter(lambda e: e.date == CurrentDateStore().current_date, events)

        row_data = map(lambda e: (e.id, e.date, e.title), events)

        self.data_table = MDDataTable(
            size_hint=(1, 8),
            use_pagination=True,
            column_data=[
                ("Id", dp(20)),
                ("Date", dp(30)),
                ("Title", dp(30)),
            ],
            rows_num=10,
            row_data=row_data
        )

        self.data_table.bind(on_row_press=self.on_date_click)

        return MDScreen(
            MDBoxLayout(
                 MDBoxLayout(
                    MDIconButton(icon="arrow-left", on_press=self.go_back),
                    MDLabel(text="Manage Events", font_style="H3"),
                    MDFloatingActionButton(icon="plus", on_press=self.open_add_dialog),
                    adaptive_height=True
                ),
                self.data_table,
                padding=[12, 10],
                pos_hint={"top": 1},
                spacing="12dp",
                orientation="vertical",
                id="manage_dates_screen_box",
            ),
            name="manage_dates",
        )

    def on_date_click(self, _, instance_row):
        pass

    def open_add_dialog(self, _):
        if not self.add_dialog:
            self.add_dialog = self.get_dialog_template(
                f"Add new event",
                self.close_relation_add,
                self.save_relation,
                lambda x: x,
            )

        self.add_dialog.open()

    def go_back(self, _):
        root_box = self.root.ids.root_box
        screen_manager_content = root_box.ids.screen_manager_content
        screen_manager_content.current = "dates"