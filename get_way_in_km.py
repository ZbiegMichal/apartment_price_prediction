import requests
import json

# TomTom API configuration
api_url = "https://api.tomtom.com/routing/1/calculateRoute/"
api_key = "rtLSxMF0tktG3uyE2BN6BTuCVAJ8ubi6"

# Coordinates
source_lat = 51.5560241
source_lon = -0.2817075
dest_lat = 53.4630621
dest_lon = -2.2935288

# Construct the API URL
tomtom_url = f"{api_url}{source_lat},{source_lon}:{dest_lat},{dest_lon}/json?key={api_key}"

try:
    # Make the API request
    response = requests.get(tomtom_url)
    response.raise_for_status()  # Raise an error for bad responses
    json_response = response.json()

    # Extract distance from the response
    distance = json_response['routes'][0]['summary']['lengthInMeters']

    # Print the distance
    print("Distance to destination is:", distance, "meters")
except requests.exceptions.RequestException as e:
    print("Error making API request:", e)
except KeyError:
    print("Error parsing API response. Check the response format.")
except json.JSONDecodeError:
    print("Error decoding JSON. Check the response content.")
