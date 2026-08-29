from abc import ABC, abstractmethod
from models.vehicle import VehicleType

class PricingStrategy:
    @abstractmethod
    def compute(self, trip):
        pass

BASE_RATES = {
    VehicleType.MINI:  {"base": 30.0, "per_km": 10.0, "per_min": 1.0},
    VehicleType.SEDAN: {"base": 50.0, "per_km": 14.0, "per_min": 1.5},
    VehicleType.SUV:   {"base": 80.0, "per_km": 20.0, "per_min": 2.0},
}


class DistanceAndTimeBasedPricing(PricingStrategy):
    '''
    Fare = base + per-km × distance + per-minute × duration.
    '''
    def compute(self, trip) -> float:
        if trip.started_at is None or trip.completed_at is None:
            raise ValueError(
                "Cannot compute distance-and-time-based fare before "
                "the trip has completed. Use a different strategy for "
                "pre-trip estimates."
            )

        if trip.vehicle is None:
            raise ValueError(
                "Cannot compute fare for a trip with no vehicle assigned."
            )

        rates = BASE_RATES[trip.vehicle.type]
        distance = trip.distance_km()
        duration_min = (
            trip.completed_at - trip.started_at
        ).total_seconds() / 60


        return (
            rates["base"]
            + rates["per_km"] * distance
            + rates["per_min"] * duration_min
        )

class FlatRatePricing(PricingStrategy):
    def __init__(self, flat_amount: float):
        self.flat_amount = flat_amount

    def compute(self, trip) -> float:
        return self.flat_amount


