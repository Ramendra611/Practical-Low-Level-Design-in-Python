"""

Central entity of the ride sharing app
"""

from datetime import datetime
from typing import Optional
import uuid


class Trip:

    def __init__(self, rider, source, destination, vehicle_type):
        self.id: str = str(uuid.uuid4())
        self.rider = rider
        self.source = source
        self.destination = destination
        self.requested_vehicle_type = vehicle_type  # what is requested

        ## driver and vehicle assigned
        self.driver = None
        self.vehicle = None

        ## information about the trip
        self.started_at: Optional[datetime] = None
        self.completed_at: Optional[datetime] = None
        self.fare: Optional[float] = None
        self.cancellation_fee: Optional[float] = None

        self.rider_rating_of_driver: Optional[int] = None
        self.driver_rating_of_rider: Optional[int] = None

        from states.requested import Requested

        self.state = Requested()

    def assign_driver(self, driver):
        self.state.assign_driver(self, driver)

    def start(self):
        self.state.start(self)

    def complete(self, fare):
        self.state.complete(self, fare)

    def cancel(self):
        self.state.cancel(self)


    def distance_km(self) -> float:
        """Straight-line distance from source to destination in km."""
        return self.source.distance_to(self.destination)

    def __repr__(self) -> str:
        return (
            f"Trip(id={self.id[:8]}..., state={self.state.name()}, "
            f"rider={self.rider.name!r})"
        )

