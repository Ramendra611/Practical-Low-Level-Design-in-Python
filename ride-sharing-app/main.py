##  create a manager

from manager import TripManager
from strategies.cancellation import CancellationPolicy
from strategies.matching import NearestDriverStrategy
from strategies.pricing import DistanceAndTimeBasedPricing, FlatRatePricing

from models.driver import  Driver
from models.rider import Rider
from models.vehicle import  VehicleType, Vehicle
from models.location import Location
from strategies.payment import UPIPayment

ride_manager = TripManager(matching=NearestDriverStrategy(),
                           pricing=DistanceAndTimeBasedPricing(),
                           cancellation=CancellationPolicy())

driver1 = Driver(
    "d101",
    "Arjun Verma",
    "98765-1001",
    Vehicle("KA01AB1234", VehicleType.SEDAN, "Honda City"),
    Location(12.9716, 77.5946),
)
driver2 = Driver(
    "d102",
    "Meera Nair",
    "98765-1002",
    Vehicle("MH12CD5678", VehicleType.MINI, "Maruti WagonR"),
    Location(12.9820, 77.6005),
)

ride_manager.register_driver(driver1)
ride_manager.register_driver(driver2)

# Create rider
rider = Rider("r201", "Ananya Patel", "98765-2001")


# Request ride
trip = ride_manager.request_ride(
    rider=rider,
    source=Location(12.9716, 77.5946),
    destination=Location(12.9500, 77.5500),
    vehicle_type=VehicleType.SEDAN,
)

print("Assigned driver:", trip.driver.name if trip.driver else "None")


# Start trip
ride_manager.start_trip(trip.id)

# Complete trip with UPI
fare = ride_manager.complete_trip(trip.id, UPIPayment("ananya@upi"))
print("Final fare:", fare)


# Rate trip
ride_manager.rate_trip(trip.id, by_rider=5, by_driver=4)
print("Driver rating:", trip.driver.rating)
print("Rider rating:", trip.rider.rating)
print("Trip state:", trip.state.name())