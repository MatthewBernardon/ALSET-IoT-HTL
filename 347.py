##############################################################################################################################


 #If the car detects that it will hit an object in front of it, 
 #the car will automatically apply the brakes to avoid the collision.
 #Speeds are in m/s, distances are in meters, and time is in seconds.
def automatic_breaking(car_speed: float, object_detected_distance: float, road_is_slick: bool) -> bool:
    if car_speed > 0:
        time_to_collision = object_detected_distance / car_speed
        if road_is_slick:
            time_to_collision = time_to_collision / 1.5
        if time_to_collision <= 3:
            print("Potential collision detected! Automatic breaking initiated.")
            return True
    return False


def test_automatic_breaking():
    assert automatic_breaking(50, 100, False) == True
    assert automatic_breaking(50, 100, True) == True
    assert automatic_breaking(50, 300, False) == False
    assert automatic_breaking(0, 100, False) == False
    assert automatic_breaking(50, 0, False) == True
    print("\n")


##############################################################################################################################


# In an area with clearly defined lanes, if the car is in Assisted-Driving 
# mode and the driver is beginning to veer from the lane unintentionally, 
# the car will notify the driver and hold the Vechicle steady.
# direction_of_creep is a float between -1 and 1 (-1 is left, 0 is straight, 1 is right)
def driver_assisted_steering_correction(car_speed: float, turn_signal: bool, out_of_lane: bool, direction_of_creep: float) -> float:
    if car_speed > 0 and not turn_signal and out_of_lane:
        if direction_of_creep < -0.25:
            print("Driver assisted steering correction initiated: steering right.")
            return -direction_of_creep
        elif direction_of_creep > 0.25:
            print("Driver assisted steering correction initiated: steering left.")
            return -direction_of_creep
    return 0


def test_driver_assisted_steering_correction():
    assert driver_assisted_steering_correction(50, False, True, -0.5) == 0.5
    assert driver_assisted_steering_correction(50, False, True, 0.5) == -0.5
    assert driver_assisted_steering_correction(50, False, True, 0) == 0
    assert driver_assisted_steering_correction(0, False, True, 0) == 0
    assert driver_assisted_steering_correction(50, True, True, 0) == 0
    print("\n")


##############################################################################################################################


# The car will always be able to locate all the charging stations that can be reached with its current battery level
def charging_station_navigation(battery_percentage: float, driver_prompt: bool, \
                    miles_remaining: float, distances_to_charging_stations: list) -> list:
    if battery_percentage < 15 or driver_prompt:
        vdistances = []
        for distance in distances_to_charging_stations:
            if distance <= miles_remaining:
                vdistances.append(distance)
        vdistances.sort()
        return vdistances
    return []


def test_charging_station_navigation():
    assert charging_station_navigation(50, True, 250, [10, 20, 30, 40, 50]) == [10, 20, 30, 40, 50]
    assert charging_station_navigation(5, False, 25, [20, 10, 30, 50, 40]) == [10, 20]
    assert charging_station_navigation(50, False, 250, [20, 30, 22, 10, 55]) == []
    assert charging_station_navigation(14, True, 70, [10, 22, 33, 44, 77, 88]) == [10, 22, 33, 44]
    assert charging_station_navigation(8, False, 40, [11, 35, 22, 41, 56, 70]) == [11, 22, 35]


##############################################################################################################################


# When prompted by the driver, the vehicle should automatically gather necessary
# navigation data and transistion to Self-Driving mode if a destination is set.
def assisted_driving_to_self_driving_transition(mode: str, destination_set: bool, can_transition: bool) -> bool:
    if mode == "assisted-driving" and destination_set and can_transition:
        mode = "self-driving"
        print("Transitioning from assisted driving to self-driving.")
        return True
    if not destination_set:
        print("Destination not set, cannot transition.")
    elif not can_transition:
        print("Transition currently not possible.")
    return False


def test_assisted_driving_to_self_driving_transition():
    assert assisted_driving_to_self_driving_transition("assisted-driving", True, True) == True
    assert assisted_driving_to_self_driving_transition("assisted-driving", False, True) == False
    assert assisted_driving_to_self_driving_transition("assisted-driving", True, False) == False
    assert assisted_driving_to_self_driving_transition("self-driving", True, True) == False
    assert assisted_driving_to_self_driving_transition("self-driving", False, False) == False
    print("\n")


##############################################################################################################################


# The Car will detect when the driver wants to park
# and can park by itself if the driver wishes.
def parking_assistance(speed: float, nearby_parking_spaces: bool, user_authorization: bool, mode: str) -> bool:
    if speed <= 10 and nearby_parking_spaces and user_authorization and mode == "assisted-driving":
        print("Parking assistance initiated.")
        mode = "self-parking"
        return True
    return False


def test_parking_assistance():
    assert parking_assistance(10, True, True, "assisted-driving") == True
    assert parking_assistance(7, True, True, "self-driving") == False
    assert parking_assistance(8, True, False, "assisted-driving") == False
    assert parking_assistance(9, False, True, "assisted-driving") == False
    assert parking_assistance(20, True, True, "assisted-driving") == False
    print("\n")


##############################################################################################################################


# When a location is put into the console, the car will plot an optimal route
# to the location given GPS data and local traffic data.
def route_plotting(destination: str, gps: list, traffic: str) -> list:
    # find_routes simulates the car calculating all possible routes to a
    # destination and returns a list of times in minutes to display to the driver
    if destination != "":
        routes = find_routes(destination, gps, traffic)
        routes.sort()
        print(destination)
        for i in range(3):
            print("Route", i+1, ":", routes[i], "minutes.")
        print("\n")
        return routes[:3]
    return []


def test_route_plotting():
    assert route_plotting("Home", "GPSData", "WeatherData") == [4, 6, 9]
    assert route_plotting("Work", "GPSData", "WeatherData") == [22, 24, 28]
    assert route_plotting("School", "GPSData", "WeatherData") == [13, 14, 17]
    assert route_plotting("Walmart", "GPSData", "WeatherData") == [34, 44, 48]
    assert route_plotting("", "GPSData", "WeatherData") == []
    print("\n")


def find_routes(a, b, c):
    if a == "Walmart": return [48, 34, 58, 62, 44]
    if a == "Work": return [28, 24, 32, 30, 22]
    if a == "School": return [14, 13, 19, 22, 17]
    if a == "Home": return [4, 10, 6, 18, 9]
    


##############################################################################################################################


# Should the driver press a designated "Emergency" button on the console, the
# vehicle will immediately take control and attempt to pull-over at a safe location
def emergency_pullover(mode: str, distance_to_pullover: float) -> bool:
    mode = "self-driving"
    print("Attempting to pull over to location in", distance_to_pullover, "meters.")
    return True


def test_emergency_pullover():
    assert emergency_pullover("assisted-driving", 100) == True
    assert emergency_pullover("self-driving", 100) == True
    assert emergency_pullover("assisted-driving", 10) == True
    assert emergency_pullover("self-driving", 20) == True
    assert emergency_pullover("assisted-driving", 50) == True
    print("\n")


##############################################################################################################################


# Upon detection of emergency vehicles, if the car is in Self-Driving mode
# it will immediately notify the driver and attempt to pull over
def emergency_vehicle_detection_and_response(speed: float, mode: str, emergency_vehicle_detected: bool) -> bool:
    if speed > 0 and mode == "self-driving" and emergency_vehicle_detected:
        print("Emergency vehicle detected! Initiating pull over.")
        return True
    return False


def test_emergency_vehicle_detection_and_response():
    assert emergency_vehicle_detection_and_response(55, "self-driving", True) == True
    assert emergency_vehicle_detection_and_response(69, "assisted-driving", True) == False
    assert emergency_vehicle_detection_and_response(0, "self-driving", True) == False
    assert emergency_vehicle_detection_and_response(13, "self-driving", False) == False
    assert emergency_vehicle_detection_and_response(24, "assisted-driving", False) == False
    print("\n")


##############################################################################################################################


# If the car detects that it has been in an accident,
# it will stop and contact emergency services.
def crash_detection(potential_collision_detected: bool, speed: float, acceleration: float) -> bool:
    if potential_collision_detected and speed == 0 and acceleration < -20:
        print("Crash detected! Halting all operations and contacting emergency services.")
        return True
    return False


def test_crash_detection():
    assert crash_detection(True, 10, 0) == False
    assert crash_detection(True, 0, -4) == False
    assert crash_detection(True, 0, -100) == True
    assert crash_detection(True, 10, -21) == False
    assert crash_detection(False, 0, -21) == False
    print("\n")


##############################################################################################################################


# Car correctly interprets all driver steering commands 
# and disables Self-Driving if it is active.
def self_driving_to_assisted_driving_transition(speed: float, mode: str, driver_input: bool):
    if speed > 0 and mode == "self-driving" and driver_input:
        mode = "assisted-driving"
        print("Driver control resumed. Turning off Self-Driving.")
        return True
    return False


def test_self_driving_to_assisted_driving_transition():
    assert self_driving_to_assisted_driving_transition(30, "self-driving", True) == True
    assert self_driving_to_assisted_driving_transition(60, "self-driving", False) == False
    assert self_driving_to_assisted_driving_transition(0, "self-driving", True) == False
    assert self_driving_to_assisted_driving_transition(20, "assisted-driving", True) == False
    assert self_driving_to_assisted_driving_transition(50, "assisted-driving", False) == False
    print("\n")


##############################################################################################################################


# If the car is locked and the key fob is brought within 5 feet of the car, the car will unlock.
# If the car is unlocked and the key fob is taken more than 5 feet away, the car will lock.
def key_fob_auto_lock_unlock(new_key_distance: float, old_key_distance: float, locked: bool) -> bool:
    if locked and new_key_distance <= 5 and old_key_distance > 5:
        locked = False
        return False
    elif not locked and new_key_distance > 5 and old_key_distance <= 5:
        locked = True
        return True
    return locked
    
    
def test_key_fob_auto_lock_unlock():
    assert key_fob_auto_lock_unlock(4, 12, True) == False
    assert key_fob_auto_lock_unlock(18, 9, False) == False
    assert key_fob_auto_lock_unlock(3, 11, False) == False
    assert key_fob_auto_lock_unlock(12, 5, True) == True
    assert key_fob_auto_lock_unlock(10, 10, True) == True
    
##############################################################################################################################

CONST_USERNAME = "Milind"
CONST_PASSWORD = "KDog2004"

# Technichian login. If an incorrect username or password is entered 3 times, the login will lock.
# Returns true on unlock, false on failed attempt.
# Note: default login, password is Milind, KDog2004
def technichian_login(username: str, password: str, trys: int = 0):
    if trys >= 3:
        print("Login locked.")
        return False
    if username == CONST_USERNAME and password == CONST_PASSWORD:
        print("Login successful.")
        return True
    print("Inncorrect username or password.")
    return False


def test_technichian_login():
    assert technichian_login("Milind", "KDog2004") == True
    assert technichian_login("Milind", "KDog2004", 4) == False
    assert technichian_login("Nilind", "KCat2004") == False
    assert technichian_login("Milind", "KDog2004", 1) == True
    assert technichian_login("Milind", "KDog2003", 2) == False
    print("\n")

test_automatic_breaking()
test_driver_assisted_steering_correction()
test_charging_station_navigation()
test_assisted_driving_to_self_driving_transition()
test_parking_assistance()
test_route_plotting()
test_emergency_pullover()
test_emergency_vehicle_detection_and_response()
test_crash_detection()
test_self_driving_to_assisted_driving_transition()
test_key_fob_auto_lock_unlock()
test_technichian_login()
print("All tests passed!")