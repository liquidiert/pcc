from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.uix.button import MDIconButton

import calendar
from datetime import datetime
from dateutil.relativedelta import relativedelta

import objectbox
from models.date import Date
from objectbox_handler import ob

from store.current_date import CurrentDateStore

from functools import partial

class DatesScreen:
    layout = None
    current_date = datetime.now()
    root = None
    dates_box = objectbox.Box(ob, Date)
    manage_screen = None

    def init(self, root, sub_screen):
        self.root = root
        self.manage_screen = sub_screen

    def build(self):
        current_days = calendar.monthrange(self.current_date.year, self.current_date.month)

        to_display = self.build_day_cards(current_days[1])

        self.layout = MDGridLayout(
                    cols=7,
                    spacing="10dp",
                    adaptive_height=True,
                    size_hint=(1, 1)
                )
        
        for card in to_display:
            self.layout.add_widget(card)

        return MDScreen(
            MDBoxLayout(
                MDLabel(text="Events management", font_style="H3", adaptive_height=True),
                MDBoxLayout(
                    MDIconButton(
                        icon="chevron-left",
                        on_press=self.previous_month
                    ),
                    MDLabel(
                        text=f"{self.current_date.month}-{self.current_date.year}",
                        pos_hint={"y": .025},
                        adaptive_width=True,
                        halign="center",
                        id="current_date_range"
                    ),
                    MDIconButton(
                        icon="chevron-right",
                        on_press=self.next_month
                    ),
                    adaptive_height=True,
                    id="date_select_box"
                ),
                self.layout,
                padding=[12, 10],
                pos_hint={"top": 1},
                orientation="vertical",
                spacing="12dp",
                id="events_box"
            ),
            name="events",
        )
    
    def refresh(self):
        self.layout.clear_widgets()
        
        current_days = calendar.monthrange(self.current_date.year, self.current_date.month)

        to_display = self.build_day_cards(current_days[1])

        for day in to_display:
            self.layout.add_widget(day)
    
    def build_day_cards(self, date_range: int):

        events = self.dates_box.get_all()

        to_display = []
        for x in range(1, date_range + 1):
            event_count = len(list(filter(lambda e: e.date == f'{x}-{self.current_date.month}-{self.current_date.year}', events)))

            to_display.append(
                MDCard(
                    MDRelativeLayout(
                        MDIconButton(
                            icon="dots-vertical",
                            pos_hint={"top": 1, "right": 1},
                            on_press=partial(self.on_day_click, x)
                        ),
                        MDLabel(
                            text=f"{x}.",
                            adaptive_size=True,
                            padding=8,
                            pos_hint={"top": 1,"left": 0}
                        ),
                        MDLabel(
                            text=f"{event_count} events",
                            theme_text_color="Primary" if event_count != 0 else "Hint",
                            pos_hint={"center_x": 0.7, "center_y": 0.3}
                        )
                    ),
                    padding=4,
                    size_hint=(1, None),
                    line_color=(0.2, 0.2, 0.2, 0.8),
                    style="outlined",
                    shadow_offset=(0, -1)
                )
            )
        return to_display

    def on_day_click(self, day, _):
        CurrentDateStore.current_date = f"{day}-{self.current_date.month}-{self.current_date.year}"

        self.manage_screen.refresh()

        root_box = self.root.ids.root_box
        screen_manager_content = root_box.ids.screen_manager_content
        screen_manager_content.current = "manage_dates"

    def previous_month(self, _):
        self.layout.clear_widgets()
        
        self.current_date = self.current_date - relativedelta(months=1)
        current_days = calendar.monthrange(self.current_date.year, self.current_date.month)

        to_display = self.build_day_cards(current_days[1])

        for day in to_display:
            self.layout.add_widget(day)

        self.set_current_date_label()

    def next_month(self, _):
        self.layout.clear_widgets()
        
        self.current_date = self.current_date + relativedelta(months=1)
        current_days = calendar.monthrange(self.current_date.year, self.current_date.month)

        to_display = self.build_day_cards(current_days[1])

        for day in to_display:
            self.layout.add_widget(day)

        self.set_current_date_label()

    def set_current_date_label(self):
        root_box = self.root.ids.root_box
        screen_manager_content = root_box.ids.screen_manager_content
        screen_manager_content.get_screen("dates").ids.dates_box.ids.date_select_box.ids.current_date_range.text = f"{self.current_date.month}-{self.current_date.year}"