import pydantic_ai
print(f"Version: {pydantic_ai.__version__}")
from pydantic_ai import Agent
import inspect

# Inspect the return type of Agent.run
print(f"Agent.run return annotation: {inspect.signature(Agent.run).return_annotation}")
