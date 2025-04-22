from ambulance_service import book_ambulance, notify_nearby_hospitals
from location_service import get_current_location

def test_emergency_system():
    print("Testing location service...")
    loc, addr = get_current_location()
    print(f"Location: {loc}, Address: {addr}")
    
    print("\nTesting ambulance booking...")
    booking = book_ambulance(loc[0], loc[1])
    print(f"Booking result: {booking}")
    
    print("\nTesting hospital notification...")
    hospitals = notify_nearby_hospitals(loc[0], loc[1])
    print("Nearby hospitals:")
    for h in hospitals:
        print(f"- {h['name']} ({h['distance']}): {h['contact']}")

if __name__ == "__main__":
    test_emergency_system()