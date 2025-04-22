import webbrowser
import random

def book_ambulance(lat, lng):
    """Simulate ambulance booking with local hospital data"""
    hospitals = [
        {"name": "City General Hospital", "distance": "2.5 km", "contact": "108"},
        {"name": "Metro Medical", "distance": "3.1 km", "contact": "102"}
    ]
    
    return {
        "success": True,
        "ambulance_id": f"AMB{random.randint(1000,9999)}",
        "eta": random.randint(5, 15),
        "driver_name": f"Driver {random.choice(['John', 'Priya'])}",
        "tracking_url": "https://www.google.com/maps?q=" + f"{lat},{lng}"  # Open Google Maps
    }

def notify_nearby_hospitals(lat, lng):
    """Simulate hospital notification"""
    return [
        {"name": "City General", "contact": "108", "specialties": ["Emergency"]},
        {"name": "Metro Trauma", "contact": "102", "specialties": ["Accident"]}
    ]

def open_tracking_interface(tracking_url):
    """Open tracking in browser"""
    webbrowser.open(tracking_url)
    print(f"Tracking opened at: {tracking_url}")