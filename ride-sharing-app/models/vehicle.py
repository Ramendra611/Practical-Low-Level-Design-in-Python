from enum import Enum
from dataclasses import dataclass


class VehicleType(Enum):
    MINI = "mini"
    SEDAN = "sedan"
    SUV = "suv"

@dataclass
class Vehicle:
    plate: str
    type: VehicleType
    model: "str" = ""

    def __repr__(self) -> str:
        return f"Vehicle(plate={self.plate!r}, type={self.type.value})"
