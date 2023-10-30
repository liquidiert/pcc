from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationrail import (
    MDNavigationRail,
    MDNavigationRailItem,
)
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager

from screens.clients import ClientScreen
from screens.relations import RelationsScreen
from screens.add_relations import AddRelationsScreen
from screens.documents import DocumentsScreen
from screens.manage_documents import ManageDocumentsScreen
from screens.events import EventsScreen
from screens.manage_events import ManageEventsScreen

from kivy.core.window import Window

Window.size = (1000, 750)

import objectbox
from objectbox_handler import ob
from models.client import Client
from models.relation import Relation

import os, configparser

client_box = objectbox.Box(ob, Client)
relation_box = objectbox.Box(ob, Relation)


class PccApp(MDApp):
    client_screen = ClientScreen()
    relations_screen = RelationsScreen()
    add_relations_screen = AddRelationsScreen()
    documents_screen = DocumentsScreen()
    manage_documents_screen = ManageDocumentsScreen()
    events_screen = EventsScreen()
    manage_events_screen = ManageEventsScreen()

    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Orange"
        self.icon = "assets/pcc_icon.png"

        return MDScreen(
            MDBoxLayout(
                MDNavigationRail(
                    MDNavigationRailItem(
                        text="Clients",
                        icon="account-multiple",
                    ),
                    MDNavigationRailItem(
                        text="Relations",
                        icon="account-multiple",
                    ),
                    MDNavigationRailItem(
                        text="Documents",
                        icon="file-document-multiple",
                    ),
                    MDNavigationRailItem(
                        text="Events",
                        icon="calendar-range",
                    ),
                    id="navigation_rail",
                    md_bg_color="#fffcf4",
                    selected_color_background="#e7e4c0",
                    ripple_color_item="#e7e4c0",
                ),
                MDScreenManager(
                    self.client_screen.build(self.theme_cls, self.refresh),
                    self.relations_screen.build(),
                    self.add_relations_screen.build(self.theme_cls),
                    self.documents_screen.build(),
                    self.manage_documents_screen.build(),
                    self.events_screen.build(),
                    self.manage_events_screen.build(self.theme_cls),
                    id="screen_manager_content",
                ),
                id="root_box",
            ),
        )

    def switch_screen(self, *args, screen_manager_content=None):
        """
        Called when tapping on rail menu items. Switches application screens.
        """

        _, instance_navigation_rail_item = args
        screen_manager_content.current = instance_navigation_rail_item.text.lower()

    def refresh(self):
        self.relations_screen.refresh()
        self.documents_screen.refresh()

    def on_start(self):
        root_box = self.root.ids.root_box
        navigation_rail = root_box.ids.navigation_rail
        screen_manager_content = root_box.ids.screen_manager_content

        navigation_rail.bind(
            on_item_release=lambda *args: self.switch_screen(
                *args, screen_manager_content=screen_manager_content
            )
        )

        self.relations_screen.init(self.root, self.add_relations_screen)
        self.add_relations_screen.init(self.root)
        self.documents_screen.init(self.root, self.manage_documents_screen)
        self.manage_documents_screen.init(self.root)
        self.events_screen.init(self.root, self.manage_events_screen)
        self.manage_events_screen.init(self.root, self.events_screen)


if __name__ == "__main__":
    app_base_path = os.path.expanduser("~/.pcc")

    if not os.path.isdir(app_base_path):
        os.makedirs(app_base_path)

    # init objectbox data if user starts application for the first time

    config = None

    if not os.path.exists(f"{app_base_path}/.pcc.ini"):
        parser = configparser.ConfigParser()
        parser["DEFAULT"] = {"hasAppOpened": "no"}
        with open(f"{app_base_path}/.pcc.ini", "w+") as config_file:
            parser.write(config_file)

        config = parser
    else:
        parser = configparser.ConfigParser()
        parser.readfp(open(f"{app_base_path}/.pcc.ini"))

        config = parser

    if config["DEFAULT"]["hasAppOpened"] == "no":
        test_client = Client()
        test_client.firstname = "Korbinian"
        test_client.lastname = "Habereder"
        test_client.country = "Deutschland"
        test_client.zip = "84688"
        test_client.city = "Teststadt"
        test_client.street = "Teststraße"
        test_client.number = "5"
        test_client.birthdate = 926952165

        client_id = client_box.put(test_client)

        test_relation = Relation()
        test_relation.type = "Relative"
        test_relation.firstname = "L"
        test_relation.lastname = "Habereder"
        test_relation.country = "Deutschland"
        test_relation.zip = "84688"
        test_relation.city = "Teststadt"
        test_relation.street = "Teststraße"
        test_relation.number = "5"
        test_relation.client_id = client_id

        relation_box.put(test_relation)

        with open(f"{app_base_path}/.pcc.ini", "w") as config_file:
            config["DEFAULT"]["hasAppOpened"] = "yes"
            print(config)
            config.write(config_file)

    PccApp().run()
