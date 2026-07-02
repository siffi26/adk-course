from google.adk.tools import ToolContext


QUESTIONS = [
    "What is the difference between an LLM and an agent?",
    "When would you use tools with an LLM?",
    "What is structured output and why is it useful?",
    "What is the difference between session state and user state?",
    "Why should task progress usually be stored in session state?",
]


def set_iterations(num_iterations: int, tool_context: ToolContext) -> str:
    """Set how many questions the user wants to answer in future sessions."""

    if num_iterations < 1:
        return "Please choose at least 1 question."

    if num_iterations > len(QUESTIONS):
        return f"Please choose {len(QUESTIONS)} questions or fewer."

    tool_context.state["user:num_iterations"] = num_iterations

    tool_context.state["user:num_iterations_instructions"] = """
We already know how many questions the user wants to answer.
You should start asking questions by calling the run_task tool.
"""

    return f"I'll remember that you want me to ask you {num_iterations} questions."


def run_task(tool_context: ToolContext) -> dict:
    """Ask the next question based on the user's saved preference and session progress."""

    num_iterations = tool_context.state.get("user:num_iterations", 1)
    current_iteration = tool_context.state.get("current_iteration", 0)

    if current_iteration < num_iterations:
        question = QUESTIONS[current_iteration]
        current_iteration += 1

        tool_context.state["current_iteration"] = current_iteration

        return {
            "complete": False,
            "current_iteration": current_iteration,
            "num_iterations": num_iterations,
            "question": question,
        }

    return {
        "complete": True,
        "message": "You have completed all your questions.",
    }