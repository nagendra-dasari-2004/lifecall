import requests
from pprint import pprint

GEOAPIFY_API_KEY = "7e3060986bbd458daad681f933b6d6f7"  # Get from geoapify.com

def get_precise_location():
    """Get precise location using Geoapify without area-specific logic"""
    try:
        # Step 1: Get coordinates (IP-based)
        ip_data = requests.get('https://ipapi.co/json/', timeout=3).json()
        lat, lng = ip_data.get('latitude'), ip_data.get('longitude')
        
        if not lat or not lng:
            return None, "Could not get coordinates"
        
        # Step 2: Get precise address using Geoapify
        url = f"https://api.geoapify.com/v1/geocode/reverse?lat={lat}&lon={lng}&apiKey={GEOAPIFY_API_KEY}"
        response = requests.get(url).json()
        
        if not response['features']:
            return (lat, lng), "Address not found"
        
        # Extract complete address components
        properties = response['features'][0]['properties']
        address = {
            'road': properties.get('street'),
            'neighborhood': properties.get('suburb'),
            'city': properties.get('city'),
            'state': properties.get('state'),
            'postcode': properties.get('postcode'),
            'country': properties.get('country')
        }
        
        # Format address string
        address_parts = [
            address['road'],
            address['neighborhood'],
            f"{address['city']}, {address['state']}",
            address['postcode'],
            address['country']
        ]
        formatted_address = ", ".join(filter(None, address_parts))
        
        return (lat, lng), formatted_address
        
    except requests.exceptions.RequestException as e:
        print(f"Network error: {e}")
        return None, "Network error"
    except Exception as e:
        print(f"Unexpected error: {e}")
        return None, "Location service error"

# Usage Example
if __name__ == "__main__":
    print("Detecting location...")
    coords, address = get_precise_location()
    
    if coords:
        print(f"\nCoordinates: {coords}")
        print("Full Address Details:")
        pprint(address)  # Pretty print full address
    else:
        print(f"\nError: {address}")