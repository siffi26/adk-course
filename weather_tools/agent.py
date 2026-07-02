import os
from google.adk.agents import Agent

def get_temperature(city: str) -> str:
    """Returns the temperature in a city."""
    return f"The temperature in {city} is 25 degrees Celsius."

def get_precipitation(city: str) -> str:
    """Returns the precipitation in a city."""
    return f"The precipitation in {city} is 10%."

def get_wind_speed(city: str) -> str:
    """Returns the wind speed in a city."""
    return f"The wind speed in {city} is 15 km/h."

model = "gemini-2.5-flash-lite"

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")

with open(instruction_file_path, "r") as f:
    instruction = f.read()

root_agent = Agent(
    name="weather_tools",
    description="Weather agent with tools for temperature, precipitation, and wind speed.",
    model=model,
    instruction=instruction,
    tools=[
        get_temperature,
        get_precipitation,
        get_wind_speed,
    ],
)