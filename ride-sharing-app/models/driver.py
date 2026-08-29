from models.user import User
from models.vehicle import Vehicle
from models.location import Location


class Driver(User):

    def __init__(
        self, user_id: str, name: str, phone: str, vehicle: Vehicle, location: Location
    ):
        super().__init__(user_id, name, phone)
        self.vehicle = vehicle
        self.location = location
        self.is_available = (
            True  # this is for marking the driver as available for booking
        )

    def go_online(self) -> None:
        self.is_available = True

    def go_offline(self) -> None:
        self.is_available = False
