from kivy.properties import ObjectProperty
from kivy.event import EventDispatcher

class CurrentClientStore(EventDispatcher):
    current_client = ObjectProperty(None, allownone=True)

    @property
    def has_client(self):
        return self.current_client is not None