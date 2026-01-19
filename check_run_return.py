from pydantic_ai import Agent
import inspect
sig = inspect.signature(Agent.run)
print(f"Agent.run return type: {sig.return_annotation}")
