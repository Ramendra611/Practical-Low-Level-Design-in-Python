from states.base import TripState


class Cancelled(TripState):
    def name(self) -> str:
        return "CANCELLED"

    ## terminal state
