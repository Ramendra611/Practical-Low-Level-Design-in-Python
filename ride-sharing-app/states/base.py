from abc import ABC, abstractmethod
from utils.exceptions import InvalidStateTransition


class TripState(ABC):

    @abstractmethod
    def name(self) -> str:
        """Human-readable state name — used in errors and logs."""

    def assign_driver(self, trip, driver):
        raise InvalidStateTransition(f"Cannot assign a driver in state {self.name()}")

    def start(self, trip):
        raise InvalidStateTransition(f"Cannot start a trip in state {self.name()}")

    def complete(self, trip, fare):
        raise InvalidStateTransition(f"Cannot complete a trip in state {self.name()}")

    def cancel(self, trip):
        raise InvalidStateTransition(f"Cannot cancel a trip in state {self.name()}")

    def __repr__(self) -> str:
        return f"<TripState:{self.name()}>"
