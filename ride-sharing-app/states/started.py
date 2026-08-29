from states.base import TripState
from datetime import datetime


class Started(TripState):
    def name(self) -> str:
        return "STARTED"

    def complete(self, trip, fare: float) -> None:
        trip.completed_at = datetime.now()
        trip.fare = fare

        # change the state
        from states.completed import Completed

        trip.state = Completed()

    def cancel(self, trip) -> None:
        ## change the state to cancelled
        from states.cancelled import Cancelled

        trip.state = Cancelled()
