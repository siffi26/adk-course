from google.adk.tools import ToolContext


def set_home_location(location: str, tool_context: ToolContext):
    """
    Sets the customer's home location.
    Only do this if they explicitly tell you to.
    """

    tool_context.state["user:home_location"] = location

    tool_context.state["user:home_location_instruction"] = f"""
The user's home location is {location}.
If the user does not specify a starting point for a trip, use {location} as the starting point.
"""

    return f"Home location set to {location}."


def add_city(city: str, tool_context: ToolContext):
    """
    Adds a city or airport to the current session itinerary.
    """

    itinerary = tool_context.state.get("itinerary", [])

    itinerary.append(city)

    tool_context.state["itinerary"] = itinerary

    return {
        "status": f"Added {city} to the itinerary.",
        "itinerary": itinerary,
    }


def create_itinerary(tool_context: ToolContext):
    """
    Creates the itinerary based on the cities in the current session state.
    """

    itinerary = tool_context.state.get("itinerary", [])
    home_location = tool_context.state.get("user:home_location")

    if not itinerary:
        return {
            "itinerary": [],
            "message": "No cities have been added to the itinerary yet.",
        }

    full_route = itinerary.copy()

    if home_location and full_route[0] != home_location:
        full_route = [home_location] + full_route

    legs = []

    for i in range(len(full_route) - 1):
        legs.append({
            "from": full_route[i],
            "to": full_route[i + 1],
        })

    return {
        "itinerary": legs,
    }