import os

from google.adk.agents import Agent
from question_state_agent.tools import set_iterations, run_task


model = "gemini-2.5-flash"

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")

with open(instruction_file_path, "r") as f:
    instruction = f.read()


root_agent = Agent(
    name="question_state_agent",
    description="An agent that remembers how many questions the user wants and tracks progress per session.",
    model=model,
    instruction=instruction,
    tools=[
        set_iterations,
        run_task,
    ],
)