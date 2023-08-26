from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel


class RelationsScreen:

    def build(self):
        return MDScreen(
            MDBoxLayout(
                MDLabel(
                    text="Relations",
                    font_style="H3"
                ),
                
                padding=[12, 0],
                adaptive_height=True,
                pos_hint={"top": 1},
                orientation="vertical"
            ),
            name="relations",
        )