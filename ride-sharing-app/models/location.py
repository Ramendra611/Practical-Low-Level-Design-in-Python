from dataclasses import dataclass
import math


@dataclass
class Location:

    lng: float
    lat: float

    def distance_to(self, other: "Location"):
        """
        Calculate the distance of one location from another location
        """
        dlat = self.lat - other.lat
        dlng = self.lng - other.lng
        return math.sqrt(dlat * dlat + dlng * dlng) * 111
