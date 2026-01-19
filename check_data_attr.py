import asyncio
from pydantic_ai import Agent
from pydantic import BaseModel

class OutputModel(BaseModel):
    message: str

agent = Agent('openai:gpt-4o', output_type=OutputModel)
print(f"Agent output type: {agent.output_type}")

# We can't run it, but we can check the return type of run
import inspect
sig = inspect.signature(agent.run)
print(f"agent.run signature: {sig}")
