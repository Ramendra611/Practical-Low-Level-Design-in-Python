from states.base import TripState


class Requested(TripState):

    def name(self) -> str:
        return "REQUESTED"

    def assign_driver(self, trip, driver) -> None:
        """

        :param trip:
        :param driver:
        :return:
        """

        trip.driver = driver
        trip.vehicle = driver.vehicle

        ## change the state of the trip
        from states.driver_assigned import DriverAssigned

        trip.state = DriverAssigned()

    def cancel(self, trip) -> None:
        pass
