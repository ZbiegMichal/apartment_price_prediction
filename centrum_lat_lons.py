from geopy.geocoders import Nominatim

def get_city_center_coordinates(city_name):
    geolocator = Nominatim(user_agent="my_geocoder")
    location = geolocator.geocode(city_name)
    
    if location:
        return location.latitude, location.longitude
    else:
        print(f"Could not find coordinates for {city_name}")
        return None

# Example usage:
city_name = "Paris"
center_coordinates = get_city_center_coordinates(city_name)

if center_coordinates:
    print(f"Coordinates of the center of {city_name}: {center_coordinates}")
