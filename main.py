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
from screens.dates import DatesScreen
from screens.manage_dates import ManageDatesScreen

from kivy.core.window import Window
Window.size = (1000, 750)

import objectbox
from objectbox_handler import ob
from models.client import Client

class PccApp(MDApp):

    client_screen = ClientScreen()
    relations_screen = RelationsScreen()
    add_relations_screen = AddRelationsScreen()
    documents_screen = DocumentsScreen()
    dates_screen = DatesScreen()
    manage_date_screen = ManageDatesScreen()

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
                    self.client_screen.build(self.theme_cls),
                    self.relations_screen.build(),
                    self.add_relations_screen.build(self.theme_cls),
                    self.documents_screen.build(),
                    self.dates_screen.build(),
                    self.manage_date_screen.build(self.theme_cls),
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
        self.documents_screen.init(self.root)
        self.dates_screen.init(self.root, self.manage_date_screen)
        self.manage_date_screen.init(self.root, self.dates_screen)

if __name__=="__main__":
    client_box = objectbox.Box(ob, Client)

    PccApp().run()
