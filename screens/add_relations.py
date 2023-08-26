from kivy.metrics import dp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDIconButton, MDFloatingActionButton, MDTextButton, MDFlatButton
from kivymd.uix.label import MDLabel
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.textfield import MDTextField
from kivymd.uix.dialog import MDDialog

import objectbox
from models.relation import Relation
from models.client import Client
from objectbox_handler import ob

from typing import Callable

from store.current_client import CurrentClientStore

class AddRelationsScreen:

    theme_cls = None
    data_table = None
    relations_box = objectbox.Box(ob, Relation)
    relations = None
    root = None
    relation_to_edit = None
    edit_dialog = None
    add_dialog = None

    def init(self, root):
        self.root = root

    def build(self, theme):

        self.theme_cls = theme

        self.relations: list[Relation] = self.relations_box.get_all()

        to_display = map(
            lambda r: (r.id, r.fullname, r.address),
            self.relations,
        )

        self.data_table = MDDataTable(
            size_hint=(1, 8),
            use_pagination=True,
            column_data=[
                ("Id", dp(20)),
                ("Name", dp(40)),
                ("Address", dp(100))
            ],
            row_data=to_display,
            rows_num=10
        )

        self.data_table.bind(on_row_press=self.on_relation_click)

        return MDScreen(
            MDBoxLayout(
                MDBoxLayout(
                    MDIconButton(icon="arrow-left", on_press=self.go_back),
                    MDLabel(text="Manage Relations", font_style="H3"),
                    MDFloatingActionButton(icon="plus", on_press=self.open_add_dialog),
                    adaptive_height=True
                ),
                self.data_table,
                padding=[12, 10],
                pos_hint={"top": 1},
                spacing="12dp",
                orientation="vertical",
                id="add_relations_screen_box"
            ),
            name="add_relations",
        )

    def refresh(self):
        self.relations: list[Relation] = self.relations_box.get_all()



        self.relations = filter(lambda r: r.client_id == CurrentClientStore.current_client.id, self.relations)

        self.to_display = map(
            lambda c: (c.id, c.fullname, c.address),
            self.relations,
        )

        self.data_table.row_data = self.to_display

    def go_back(self, _):
        root_box = self.root.ids.root_box
        screen_manager_content = root_box.ids.screen_manager_content
        screen_manager_content.current = "relations"

    def on_relation_click(self, _, instance_row):
        # get index of row to extract relation id
        start_indx, _ = instance_row.table.recycle_data[instance_row.index]["range"]
        relation_id = int(instance_row.table.recycle_data[start_indx]["text"])
        relation_name = instance_row.table.recycle_data[start_indx + 1]["text"]

        self.relation_to_edit = self.relations_box.get(relation_id)

        if not self.edit_dialog:

            # create edit dialog
            self.edit_dialog = self.get_dialog_template(
                f"Edit Relation - {relation_name}",
                self.close_relation_edit,
                self.save_relation,
                self.delete_relation,
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
            ) = self.get_relation_fields(self.edit_dialog)

            # set to edit text
            firstname_field.text = self.relation_to_edit.firstname
            lastname_field.text = self.relation_to_edit.lastname
            country_field.text = self.relation_to_edit.country
            zip_field.text = self.relation_to_edit.zip
            city_field.text = self.relation_to_edit.city
            street_field.text = self.relation_to_edit.street
            number_field.text = self.relation_to_edit.number

        self.edit_dialog.open()

    def open_add_dialog(self, _):

        if not self.add_dialog:
            self.add_dialog = self.get_dialog_template(
                f"Add new relation",
                self.close_relation_add,
                self.save_relation,
                lambda x: x,
            )

        self.add_dialog.open()

    # dialog build functions
    def build_dialog_content(self) -> MDBoxLayout:
        return MDBoxLayout(
            MDTextField(
                hint_text="Firstname",
                required=True if self.relation_to_edit else False,
                write_tab=False,
                multiline=False,
                helper_text="Is required!",
                helper_text_mode="on_error",
                id="firstname_field",
            ),
            MDTextField(
                hint_text="Lastname",
                required=True if self.relation_to_edit else False,
                write_tab=False,
                multiline=False,
                helper_text="Is required!",
                helper_text_mode="on_error",
                id="lastname_field",
            ),
            MDTextField(
                hint_text="Country",
                required=True if self.relation_to_edit else False,
                write_tab=False,
                multiline=False,
                helper_text="Is required!",
                helper_text_mode="on_error",
                id="country_field",
            ),
            MDBoxLayout(
                MDTextField(
                    hint_text="Zip",
                    required=True if self.relation_to_edit else False,
                    write_tab=False,
                    multiline=False,
                    helper_text="Is required!",
                    helper_text_mode="on_error",
                    id="zip_field",
                ),
                MDTextField(
                    hint_text="City",
                    required=True if self.relation_to_edit else False,
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
                    required=True if self.relation_to_edit else False,
                    write_tab=False,
                    multiline=False,
                    helper_text="Is required!",
                    helper_text_mode="on_error",
                    id="street_field",
                ),
                MDTextField(
                    hint_text="Number",
                    required=True if self.relation_to_edit else False,
                    write_tab=False,
                    multiline=False,
                    helper_text="Is required!",
                    helper_text_mode="on_error",
                    id="number_field",
                ),
                spacing="12dp",
                id="street_box",
            ),
            orientation="vertical",
            spacing="20dp",
            size_hint_y=None,
            height="480dp",
        )

    def get_dialog_template(
        self,
        title: str,
        on_cancel: Callable,
        on_save: Callable,
        on_delete: Callable,
    ) -> MDDialog:
        """
        Builds a `MDDialog` with on delete, on cancel and save functions
        """
        delete_btn = (
            MDFlatButton(
                text="DELETE",
                on_press=on_delete,
            )
            if self.relation_to_edit
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
    
    # close functions
    def close_relation_edit(self, _):
        self.edit_dialog.dismiss(force=True)
        self.edit_dialog = None
        self.relation_to_edit = None

    def close_relation_add(self, _):
        self.add_dialog.dismiss(force=True)
        self.add_dialog = None

    # save functions
    def save_relation(self, _):
        if not self.relation_to_edit:  # add new relation
            # get field references
            (
                firstname_field,
                lastname_field,
                country_field,
                zip_field,
                city_field,
                street_field,
                number_field,
            ) = self.get_relation_fields(self.add_dialog)

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

            new_relation = Relation()
            new_relation.firstname = firstname_field.text
            new_relation.lastname = lastname_field.text
            new_relation.country = country_field.text
            new_relation.zip = zip_field.text
            new_relation.city = city_field.text
            new_relation.street = street_field.text
            new_relation.number = number_field.text
            new_relation.client_id = CurrentClientStore.current_client.id

            self.relations_box.put(new_relation)

            self.close_relation_add(None)
        else:  # save existing relation
            # get field references
            (
                firstname_field,
                lastname_field,
                country_field,
                zip_field,
                city_field,
                street_field,
                number_field,
            ) = self.get_relation_fields(self.edit_dialog)

            self.relation_to_edit.firstname = firstname_field.text
            self.relation_to_edit.lastname = lastname_field.text
            self.relation_to_edit.country = country_field.text
            self.relation_to_edit.zip = zip_field.text
            self.relation_to_edit.city = city_field.text
            self.relation_to_edit.street = street_field.text
            self.relation_to_edit.number = number_field.text

            self.relations_box.put(self.relation_to_edit)
            self.close_relation_edit(None)

        self.refresh()

    # delete function
    def delete_relation(self, _):
        self.relations_box.remove(self.relation_to_edit)

        self.close_relation_edit(None)

        self.refresh()
    
    # helpers
    def get_relation_fields(self, dialog: MDDialog):
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
