from states.base import TripState
from datetime import datetime


class DriverAssigned(TripState):
    def name(self) -> str:
        return "DRIVER_ASSIGNED"

    def start(self, trip) -> None:
        trip.started_at = datetime.now()

        ## change the state
        from states.started import Started

        trip.state = Started()

    def cancel(self, trip) -> None:

        ## change the state to cancelled
        from states.cancelled import Cancelled

        trip.state = Cancelled()
