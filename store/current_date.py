from kivy.properties import StringProperty
from kivy.event import EventDispatcher

class CurrentDateStore(EventDispatcher):
    current_date = StringProperty(None, allownone=True)

    @property
    def has_date(self):
        return self.current_date is not None