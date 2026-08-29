from datetime import datetime
from typing import Optional


from utils.exceptions import (
    InvalidStateTransition,
    UnknownTripError,
    UnknownDriverError,
    DuplicateDriverError,
)

from strategies.pricing import PricingStrategy
from strategies.matching import MatchingStrategy
from strategies.cancellation import CancellationPolicy
from strategies.payment import PaymentMethod

from models.driver import Driver
from models.rider import Rider
from models.location import Location
from models.trip import Trip
from models.vehicle import VehicleType, Vehicle

from states.completed import Completed


class TripManager:
    """
    <Facade Pattern --> interface for the ride sharing app>


    - PricingStrategy
    - MatchingStrategy
    - CancellationPolicy

    - List of drivers
    - List of trips(history and active)


    - Register a driver
    - request a ride
    - start the trip
    - complete the trip
    - cancel the trip
    - rate the trip


    """

    def __init__(
        self,
        matching: MatchingStrategy,
        pricing: PricingStrategy,
        cancellation: CancellationPolicy,
    ):
        self._matching = matching
        self._pricing = pricing
        self._cancellation = cancellation

        self._drivers: dict[str, Driver] = {}
        self._trips: dict[str, Trip] = {}

    def register_driver(self, driver: Driver) -> None:
        if driver.user_id in self._drivers:
            raise DuplicateDriverError(f"Driver {driver.user_id!r} already registered")
        self._drivers[driver.user_id] = driver

    def unregister_driver(self, driver_id: str) -> None:
        self._drivers.pop(driver_id, None)

    def available_drivers(self) -> list[Driver]:
        return [d for d in self._drivers.values() if d.is_available]

    def request_ride(
        self,
        rider: Rider,
        source: Location,
        destination: Location,
        vehicle_type: VehicleType,
    ) -> Trip:

        # create a trip
        trip = Trip(rider, source, destination, vehicle_type)
        self._trips[trip.id] = trip

        ## find and assign a driver
        driver = self._matching.select(trip, list(self._drivers.values()))

        if driver is not None:
            trip.assign_driver(driver)
            driver.is_available = False

        return trip

    def start_trip(self, trip_id: str) -> None:
        trip = self._get_trip(trip_id)
        trip.start()

    def complete_trip(
        self,
        trip_id: str,
        payment_method: PaymentMethod,
    ) -> float:

        trip = self._get_trip(trip_id)

        if trip.started_at is None:
            raise InvalidStateTransition("Cannot complete a trip that never started")

        ## calculate our fare
        now = datetime.now()
        trip.completed_at = now

        base_fare = self._pricing.compute(trip)
        multiplier = (
            1  ## we can decide this multiplier based on some surge if applicable
        )
        final_fare = base_fare * multiplier
        trip.complete(final_fare)

        # take the payment
        payment_method.charge(final_fare, trip.rider)

        ## set the driver back to available
        if trip.driver is not None:
            trip.driver.is_available = True
            trip.driver.location = trip.destination

        return final_fare

    def cancel_trip(self, trip_id: str) -> float:

        trip = self._get_trip(trip_id)
        driver_at_cancel = trip.driver

        trip.cancel()

        # calculate the fee
        fee = self._cancellation.fee(trip)
        trip.cancellation_fee = fee

        if driver_at_cancel is not None:
            driver_at_cancel.is_available = True

        return fee

    def rate_trip(
        self,
        trip_id: str,
        by_rider: Optional[int] = None,
        by_driver: Optional[int] = None,
    ) -> None:
        trip = self._get_trip(trip_id)

        if not isinstance(trip.state, Completed):
            raise InvalidStateTransition("Can only rate completed trips")

        if by_rider is not None and trip.driver is not None:
            trip.rider_rating_of_driver = by_rider
            trip.driver.update_rating(by_rider)

        if by_driver is not None:
            trip.driver_rating_of_rider = by_driver
            trip.rider.update_rating(by_driver)

    # helper method
    def _get_trip(self, trip_id: str) -> Trip:
        if trip_id not in self._trips:
            raise UnknownTripError(f"Unknown trip: {trip_id}")
        return self._trips[trip_id]
