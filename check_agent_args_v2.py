from pydantic_ai import Agent
import inspect
sig = inspect.signature(Agent.__init__)
print(f"Agent.__init__ signature: {sig}")
