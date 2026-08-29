from abc import ABC, abstractmethod
from notifications.events import LibraryEvent


class LibraryEventListener(ABC):

    def on_event(self, event: LibraryEvent):
        pass
