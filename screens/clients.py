from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.dialog import MDDialog
from kivymd.uix.label import MDLabel
from kivymd.uix.textfield import MDTextField
from kivymd.uix.pickers import MDDatePicker
from kivymd.uix.button import MDTextButton, MDFlatButton, MDFloatingActionButton
from kivy.metrics import dp

import objectbox
from models.client import Client
from objectbox_handler import ob

from typing import Callable
from datetime import date, datetime


class ClientScreen:
    clients = []
    edit_dialog = None
    add_dialog = None
    theme_cls = None
    client_box = objectbox.Box(ob, Client)
    client_to_edit: Client = None  # placeholder for editing clients
    new_birthdate = None
    birthdate_err = None
    data_table = None

    def build(self, theme):
        self.theme_cls = theme

        self.clients: list[Client] = self.client_box.get_all()

        to_display = map(
            lambda c: (c.id, c.fullname, c.human_readable_birthdate, c.address),
            self.clients,
        )

        self.data_table = MDDataTable(
            size_hint=(1, 8),
            use_pagination=True,
            column_data=[
                ("Id", dp(20)),
                ("Name", dp(30)),
                ("Birthdate", dp(30)),
                ("Address", dp(100)),
            ],
            row_data=to_display,
            rows_num=10
        )

        self.data_table.bind(on_row_press=self.on_client_click)

        return MDScreen(
            MDBoxLayout(
                MDBoxLayout(
                    MDLabel(text="Clients", font_style="H3"),
                    MDFloatingActionButton(icon="plus", on_press=self.open_add_dialog),
                    adaptive_height=True,
                ),
                self.data_table,
                padding=[12, 10],
                pos_hint={"top": 1},
                spacing="12dp",
                orientation="vertical",
                id="client_screen_box",
            ),
            name="clients",
        )

    def refresh(self):
        self.clients: list[Client] = self.client_box.get_all()

        self.to_display = map(
            lambda c: (c.id, c.fullname, c.human_readable_birthdate, c.address),
            self.clients,
        )

        self.data_table.row_data = self.to_display

    def on_client_click(self, _, instance_row):
        # get index of row to extract client id
        start_indx, _ = instance_row.table.recycle_data[instance_row.index]["range"]
        client_id = int(instance_row.table.recycle_data[start_indx]["text"])
        client_name = instance_row.table.recycle_data[start_indx + 1]["text"]

        self.client_to_edit = self.client_box.get(client_id)

        if not self.edit_dialog:
            date_dialog = MDDatePicker()
            date_dialog.bind(on_save=self.save_date)

            # create edit dialog
            self.edit_dialog = self.get_dialog_template(
                f"Edit Client - {client_name}",
                date_dialog,
                self.close_client_edit,
                self.save_client,
                self.delete_client,
            )

            # get field references
            (
                firstname_field,
                lastname_field,
                country_field,
                zip_field,
                city_field,
                street_field,
                number_field,
            ) = self.get_client_fields(self.edit_dialog)

            # set to edit text
            firstname_field.text = self.client_to_edit.firstname
            lastname_field.text = self.client_to_edit.lastname
            country_field.text = self.client_to_edit.country
            zip_field.text = self.client_to_edit.zip
            city_field.text = self.client_to_edit.city
            street_field.text = self.client_to_edit.street
            number_field.text = self.client_to_edit.number

        self.edit_dialog.open()

    def open_add_dialog(self, _):
        date_dialog = MDDatePicker()
        date_dialog.bind(on_save=self.save_date)

        if not self.add_dialog:
            self.add_dialog = self.get_dialog_template(
                f"Add new client",
                date_dialog,
                self.close_client_add,
                self.save_client,
                lambda x: x,
            )

        self.add_dialog.open()

    def build_dialog_content(self, date_dialog: MDDatePicker) -> MDBoxLayout:
        return MDBoxLayout(
            MDTextField(
                hint_text="Firstname",
                required=True if self.client_to_edit else False,
                write_tab=False,
                multiline=False,
                helper_text="Is required!",
                helper_text_mode="on_error",
                id="firstname_field",
            ),
            MDTextField(
                hint_text="Lastname",
                required=True if self.client_to_edit else False,
                write_tab=False,
                multiline=False,
                helper_text="Is required!",
                helper_text_mode="on_error",
                id="lastname_field",
            ),
            MDTextField(
                hint_text="Country",
                required=True if self.client_to_edit else False,
                write_tab=False,
                multiline=False,
                helper_text="Is required!",
                helper_text_mode="on_error",
                id="country_field",
            ),
            MDBoxLayout(
                MDTextField(
                    hint_text="Zip",
                    required=True if self.client_to_edit else False,
                    write_tab=False,
                    multiline=False,
                    helper_text="Is required!",
                    helper_text_mode="on_error",
                    size_hint=(.3, None),
                    id="zip_field",
                ),
                MDTextField(
                    hint_text="City",
                    required=True if self.client_to_edit else False,
                    write_tab=False,
                    multiline=False,
                    helper_text="Is required!",
                    helper_text_mode="on_error",
                    id="city_field",
                ),
                spacing="12dp",
                id="city_box",
            ),
            MDBoxLayout(
                MDTextField(
                    hint_text="Street",
                    required=True if self.client_to_edit else False,
                    write_tab=False,
                    multiline=False,
                    helper_text="Is required!",
                    helper_text_mode="on_error",
                    id="street_field",
                ),
                MDTextField(
                    hint_text="Number",
                    required=True if self.client_to_edit else False,
                    write_tab=False,
                    multiline=False,
                    helper_text="Is required!",
                    helper_text_mode="on_error",
                    size_hint=(.3, None),
                    id="number_field",
                ),
                spacing="12dp",
                id="street_box",
            ),
            MDBoxLayout(
                MDTextButton(text="Choose Birthdate", on_press=date_dialog.open),
                MDLabel(
                    text=self.client_to_edit.human_readable_birthdate
                    if self.client_to_edit
                    else "",
                    id="birthdate_label",
                ),
                MDLabel(
                    text="Is required!",
                    theme_text_color="Error",
                    opacity=0,
                    id="birthdate_error_label",
                ),
                spacing="12dp",
                adaptive_height=True,
                id="birthdate_box",
            ),
            orientation="vertical",
            spacing="20dp",
            size_hint_y=None,
            height="480dp",
        )

    def get_dialog_template(
        self,
        title: str,
        date_dialog: MDDatePicker,
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
            if self.client_to_edit
            else None
        )

        return MDDialog(
            title=title,
            type="custom",
            content_cls=self.build_dialog_content(date_dialog),
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

    # close functions
    def close_client_edit(self, _):
        self.edit_dialog.dismiss(force=True)
        self.edit_dialog = None
        self.client_to_edit = None

    def close_client_add(self, _):
        self.add_dialog.dismiss(force=True)
        self.add_dialog = None

    # save functions
    def save_date(self, _, value: date, date_range):
        if not self.client_to_edit:  # new client
            self.new_birthdate = int(
                datetime(year=value.year, month=value.month, day=value.day).timestamp()
            )
            self.add_dialog.content_cls.ids.birthdate_box.ids.birthdate_label.text = (
                value.strftime("%d.%m.%Y")
            )
            self.add_dialog.content_cls.ids.birthdate_box.ids.birthdate_error_label.opacity = (
                0
            )
        else:  # existing client
            self.client_to_edit.birthdate = datetime(
                year=value.year, month=value.month, day=value.day
            ).timestamp()
            self.edit_dialog.content_cls.ids.birthdate_box.ids.birthdate_label.text = (
                value.strftime("%d.%m.%Y")
            )

    def save_client(self, _):
        if not self.client_to_edit:  # add new client
            if not self.new_birthdate:  # no birthdate given -> display error
                self.birthdate_err = True
                self.add_dialog.content_cls.ids.birthdate_box.ids.birthdate_error_label.opacity = (
                    1
                )
                return

            # get field references
            (
                firstname_field,
                lastname_field,
                country_field,
                zip_field,
                city_field,
                street_field,
                number_field,
            ) = self.get_client_fields(self.add_dialog)

            # validations
            if not firstname_field.text:
                firstname_field.error = True
            if not lastname_field.text:
                lastname_field.error = True
            if not country_field.text:
                country_field.error = True
            if not zip_field.text:
                zip_field.error = True
            if not city_field.text:
                city_field.error = True
            if not street_field.text:
                street_field.error = True
            if not number_field.text:
                number_field.error = True

            if (
                not firstname_field.text
                or not lastname_field.text
                or not country_field.text
                or not zip_field.text
                or not city_field.text
                or not street_field.text
                or not number_field.text
            ):
                return

            new_client = Client()
            new_client.firstname = firstname_field.text
            new_client.lastname = lastname_field.text
            new_client.country = country_field.text
            new_client.zip = zip_field.text
            new_client.city = city_field.text
            new_client.street = street_field.text
            new_client.number = number_field.text
            new_client.birthdate = self.new_birthdate

            self.client_box.put(new_client)

            self.close_client_add(None)
        else:  # save existing client
            # get field references
            (
                firstname_field,
                lastname_field,
                country_field,
                zip_field,
                city_field,
                street_field,
                number_field,
            ) = self.get_client_fields(self.edit_dialog)

            self.client_to_edit.firstname = firstname_field.text
            self.client_to_edit.lastname = lastname_field.text
            self.client_to_edit.country = country_field.text
            self.client_to_edit.zip = zip_field.text
            self.client_to_edit.city = city_field.text
            self.client_to_edit.street = street_field.text
            self.client_to_edit.number = number_field.text

            self.client_box.put(self.client_to_edit)
            self.close_client_edit(None)

        self.refresh()

    # delete functions
    def delete_client(self, _):
        self.client_box.remove(self.client_to_edit)

        self.close_client_edit(None)

        self.refresh()

    # helpers
    def get_client_fields(self, dialog: MDDialog):
        """
        Gets all textfields from a dialog as a tuple
        """
        firstname_field = dialog.content_cls.ids.firstname_field
        lastname_field = dialog.content_cls.ids.lastname_field
        country_field = dialog.content_cls.ids.country_field
        zip_field = dialog.content_cls.ids.city_box.ids.zip_field
        city_field = dialog.content_cls.ids.city_box.ids.city_field
        street_field = dialog.content_cls.ids.street_box.ids.street_field
        number_field = dialog.content_cls.ids.street_box.ids.number_field

        return (
            firstname_field,
            lastname_field,
            country_field,
            zip_field,
            city_field,
            street_field,
            number_field,
        )
