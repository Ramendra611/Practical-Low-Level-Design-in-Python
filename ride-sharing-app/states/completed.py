from states.base import TripState


class Completed(TripState):
    def name(self) -> str:
        return "COMPLETED"

    # terminal state
