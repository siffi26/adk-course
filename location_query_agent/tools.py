import os
from google.cloud import secretmanager
from google.maps.places_v1 import PlacesClient
from google.maps.places_v1.types import SearchTextRequest
import requests

PROJECT_ID = os.environ.get("GOOGLE_CLOUD_PROJECT")
SECRET_ID = "places-api-key"

def get_api_key():
    """Gets the API key from Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{SECRET_ID}/versions/latest"
    response = client.access_secret_version(name=name)
    return response.payload.data.decode("UTF-8")

def get_place_details(place1: str, place2: str):
    """Gets the address and coordinates for two places."""
    api_key = get_api_key()
    client = PlacesClient(client_options={
        "api_key": api_key,
    })

    def get_details(place_name):
        fields = ['places.displayName', 'places.formattedAddress', 'places.location']
        field_mask = ",".join(fields)
        request = SearchTextRequest(
            text_query = place_name,
        )
        response = client.search_text( request=request, metadata=[('x-goog-fieldmask', field_mask)] )
        if response and response.places:
            info = response.places[0]
            name = info.display_name.text
            address = info.formatted_address
            location = info.location
            latitude = location.latitude
            longitude = location.longitude

            return {
                "name": name,
                "address": address,
                "location": {
                    "latitude": latitude,
                    "longitude": longitude,
                }
            }

        return None

    details1 = get_details(place1)
    details2 = get_details(place2)

    return {"place1": details1, "place2": details2}

def get_route_between_places(location1: dict, location2: dict):
    """Gets the distance and duration of the route between two places."""
    api_key = get_api_key()
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "routes.distanceMeters,routes.duration",
    }

    request_body = {
        "origin": {
            "location": {
                "latLng": {
                    "latitude": location1["latitude"],
                    "longitude": location1["longitude"],
                }
            }
        },
        "destination": {
            "location": {
                "latLng": {
                    "latitude": location2["latitude"],
                    "longitude": location2["longitude"],
                }
            }
        },
        "travelMode": "DRIVE",
    }

    url = "https://routes.googleapis.com/directions/v2:computeRoutes"

    response = requests.post(
        url=url,
        headers=headers,
        json=request_body,
    )
    response.raise_for_status()  # Raise an exception for HTTP errors
    routes_data = response.json()

    if routes_data and "routes" in routes_data and routes_data["routes"]:
        route = routes_data["routes"][0]
        return {
            "distance_meters": route["distanceMeters"],
            "duration_seconds": int(route["duration"].replace("s", "")),
        }

    return None

def get_driving_distance_and_duration(origin: str, destination: str):
    """Gets driving distance and duration between two place names."""
    places = get_place_details(origin, destination)

    if not places["place1"] or not places["place2"]:
        return {"error": "Could not find one or both places."}

    loc1 = places["place1"]["location"]
    loc2 = places["place2"]["location"]

    route = get_route_between_places(loc1, loc2)

    return {
        "origin": places["place1"],
        "destination": places["place2"],
        "route": route,
    }
