from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.button import MDIconButton, MDFloatingActionButton, MDFlatButton
from kivymd.uix.dialog import MDDialog

import objectbox
from models.date import Date
from objectbox_handler import ob

from store.current_date import CurrentDateStore

from typing import Callable

class ManageDatesScreen:

    root = None
    data_table = None
    events_box = objectbox.Box(ob, Date)
    add_dialog = None
    edit_dialog = None
    date_to_edit = None
    theme_cls = None
    parent = None

    def init(self, root, parent_screen):
        self.root = root
        self.parent = parent_screen

    def build(self, theme):

        self.theme_cls = theme

        self.data_table = MDDataTable(
            size_hint=(1, 8),
            use_pagination=True,
            column_data=[
                ("Id", dp(20)),
                ("Date", dp(30)),
                ("Title", dp(50)),
            ],
            rows_num=10
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
    
    # build methods
    def refresh(self):
        events = self.events_box.get_all()

        events = filter(lambda e: e.date == CurrentDateStore().current_date, events)

        to_display = map(lambda e: (e.id, e.date, e.title), events)

        self.data_table.row_data = to_display

    def build_dialog_content(self) -> MDBoxLayout:
        return MDBoxLayout(
            MDTextField(
                hint_text="Title",
                required=True if self.date_to_edit else False,
                write_tab=False,
                multiline=False,
                helper_text="Is required!",
                helper_text_mode="on_error",
                id="title_field",
            ),
            MDTextField(
                hint_text="Notes",
                required=True if self.date_to_edit else False,
                write_tab=False,
                multiline=True,
                max_height="100dp",
                helper_text="Is required!",
                helper_text_mode="on_error",
                id="notes_field",
            ),
            orientation="vertical",
            spacing="20dp",
            size_hint_y=None,
            height="150dp",
        )

    def get_dialog_template(
        self,
        title: str,
        on_cancel: Callable,
        on_save: Callable,
        on_delete: Callable,
    ) -> MDDialog:
        """
        Builds a `MDDialog` with custom date picker, on delete, on cancel and save functions
        """
        delete_btn = (
            MDFlatButton(
                text="DELETE",
                on_press=on_delete,
            )
            if self.date_to_edit
            else None
        )

        return MDDialog(
            title=title,
            type="custom",
            content_cls=self.build_dialog_content(),
            buttons=[
                delete_btn,
                MDFlatButton(text="CANCEL", on_press=on_cancel),
                MDFlatButton(
                    text="SAVE",
                    theme_text_color="Custom",
                    text_color=self.theme_cls.primary_color,
                    on_press=on_save,
                ),
            ],
        )

    # open functions
    def on_date_click(self, _, instance_row):
        # get index of row to extract date id
        start_indx, _ = instance_row.table.recycle_data[instance_row.index]["range"]
        date_id = int(instance_row.table.recycle_data[start_indx]["text"])
        date_title = instance_row.table.recycle_data[start_indx + 2]["text"]

        self.date_to_edit = self.events_box.get(date_id)

        if not self.edit_dialog:
            self.edit_dialog = self.get_dialog_template(
                f"Edit Event - {date_title}",
                self.close_date_edit,
                self.save_date,
                self.delete_date
            )

            # get field references
            (title_field, notes_field) = self.get_date_fields(self.edit_dialog)

            # set to edit text
            title_field.text = self.date_to_edit.title
            notes_field.text = self.date_to_edit.notes

        self.edit_dialog.open()

    def open_add_dialog(self, _):
        if not self.add_dialog:
            self.add_dialog = self.get_dialog_template(
                f"Add new event",
                self.close_date_add,
                self.save_date,
                lambda x: x,
            )

        self.add_dialog.open()

    # close functions
    def close_date_edit(self, _):
        self.edit_dialog.dismiss(force=True)
        self.edit_dialog = None
        self.date_to_edit = None

    def close_date_add(self, _):
        self.add_dialog.dismiss(force=True)
        self.add_dialog = None

    # save functions
    def save_date(self, _):
        if not self.date_to_edit:  # add new date
            # get field references
            (title_field, notes_field) = self.get_date_fields(self.add_dialog)

            if not title_field.text:
                title_field.error = True
            if not notes_field.text:
                notes_field.error = True

            if not title_field.text or not notes_field.text:
                return
            
            new_date = Date()
            new_date.date = CurrentDateStore.current_date
            new_date.title = title_field.text
            new_date.notes = notes_field.text

            self.events_box.put(new_date)

            self.close_date_add(None)
        else:  # save existing date
            # get field references
            (title_field, notes_field) = self.get_date_fields(self.edit_dialog)

            self.date_to_edit.title = title_field.text
            self.date_to_edit.notes = notes_field.text

            self.events_box.put(self.date_to_edit)

            self.close_date_edit(None)
        
        self.refresh()
        self.parent.refresh()

    # delete functions
    def delete_date(self, _):
        self.events_box.remove(self.date_to_edit)

        self.close_date_edit(None)

        self.refresh()

    # helper
    def get_date_fields(self, dialog: MDDialog):
        title_field = dialog.content_cls.ids.title_field
        notes_field = dialog.content_cls.ids.notes_field

        return (
            title_field,
            notes_field
        )

    def go_back(self, _):
        root_box = self.root.ids.root_box
        screen_manager_content = root_box.ids.screen_manager_content
        screen_manager_content.current = "dates"