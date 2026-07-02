import os

from google.adk.agents import Agent
from pydantic import BaseModel, Field
from typing import Literal, Optional


DirectionType = Literal["left", "right"]
DistanceUnitsType = Literal["feet", "yards", "meters"]
CommandType = Literal["turn", "walk", "dance", "get", "error"]


class Distance(BaseModel):
    num: float = Field(..., description="Distance value.")
    units: DistanceUnitsType = Field(..., description="Distance units.")


class RobotCommand(BaseModel):
    command: CommandType = Field(...)

    direction: Optional[DirectionType] = None

    distance: Optional[Distance] = None

    object: Optional[str] = None

    error: Optional[str] = None


class RobotCommands(BaseModel):
    commands: list[RobotCommand]


model = "gemini-2.5-flash"

script_dir = os.path.dirname(os.path.abspath(__file__))

with open(os.path.join(script_dir, "agent-prompt.txt")) as f:
    instruction = f.read()


root_agent = Agent(
    name="robot_commands",
    description="Warehouse robot controller",
    instruction=instruction,
    model=model,

    # THIS IS THE IMPORTANT LINE
    output_schema=RobotCommands,
)