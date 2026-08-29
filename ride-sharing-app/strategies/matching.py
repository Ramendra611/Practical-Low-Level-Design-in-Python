from abc import ABC, abstractmethod
from typing import List, Optional

class MatchingStrategy(ABC):
    @abstractmethod
    def select(self, trip, drivers):
        pass



class NearestDriverStrategy(MatchingStrategy):

    def __init__(self, k: int = 3):

        if k < 1:
            raise ValueError("k should be more than 1")

        self.k = k

    def select(self, trip, drivers):
        """

        1. which drivers are available and with the desired vehicle
        2. rank all drivers based on the distance from trip.source
        3. find the k = 3 closest driver
        4. select the driver among with highest rating

        """

        candidates = [
            d
            for d in drivers
            if d.is_available and d.vehicle.type == trip.requested_vehicle_type
        ]

        if not candidates:
            return None

        ## sort by proximity to trip source and find top k drivers in proximity

        nearest_k = sorted(
            candidates,
            key=lambda candidate: candidate.location.distance_to(trip.source),
        )[:self.k]

        return max(nearest_k, key = lambda candidate: candidate.rating)