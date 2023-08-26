from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.navigationrail import (
    MDNavigationRail,
    MDNavigationRailItem,
)
from kivymd.uix.screen import MDScreen
from kivymd.uix.screenmanager import MDScreenManager
from kivymd.uix.fitimage import FitImage

from screens.clients import ClientScreen
from screens.relations import RelationsScreen
from screens.mail import MailScreen
from screens.settings import SettingsScreen

from kivy.core.window import Window
Window.size = (1000, 750)

import objectbox
from objectbox_handler import ob
from models.client import Client

from datetime import datetime


class PccApp(MDApp):

    client_screen = ClientScreen()
    relations_screen = RelationsScreen()
    mail_screen = MailScreen()
    settings_screen = SettingsScreen()

    def build(self):
        self.theme_cls.material_style = "M3"
        self.theme_cls.primary_palette = "Orange"

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
                        text="Mail",
                        icon="email-outline",
                    ),
                    MDNavigationRailItem(
                        text="Settings",
                        icon="cog-outline",
                    ),
                    id="navigation_rail",
                    md_bg_color="#fffcf4",
                    selected_color_background="#e7e4c0",
                    ripple_color_item="#e7e4c0",
                ),
                MDScreenManager(
                    self.client_screen.build(self.theme_cls, self.root),
                    self.relations_screen.build(),
                    self.mail_screen.build(),
                    self.settings_screen.build(),
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

if __name__=="__main__":
    client_box = objectbox.Box(ob, Client)

    if len(client_box.get_all()) == 1:
        c = Client()
        c.firstname = "Korbi"
        c.lastname = "Habi"
        c.country = "Deutschland"
        c.city = "Auerbach"
        c.zip = "94530"
        c.street = "Am Buchenhain"
        c.number = "14"
        c.birthdate = int(datetime.now().timestamp())
        client_box.put(c)
        client_box.put(c)

    PccApp().run()
