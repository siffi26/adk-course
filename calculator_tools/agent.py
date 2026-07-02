import os
from google.adk.agents import Agent

def addition(a: float, b: float) -> float:
	return a + b

def substraction(a: float, b: float) -> float:
	return a - b

def multiplication(a: float, b: float) -> float:
	return a * b

def division(a: float, b: float) -> str:
	if b == 0:
		return "Cannot divide by zero."
	return str(a / b)

model = "gemini-2.5-flash"

script_dir = os.path.dirname(os.path.abspath(__file__))
instruction_file_path = os.path.join(script_dir, "agent-prompt.txt")

with open(instruction_file_path, "r") as f:
    instruction = f.read()

tools = [
addition,
substraction,
multiplication,
division
]

root_agent = Agent(
  name="calculator_tools",
  description="Multiple tools to do different mathematical calculations",
  model=model,
  tools=tools,
  instruction=instruction,
)