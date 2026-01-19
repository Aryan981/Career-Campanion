import asyncio
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic import BaseModel

class TestModel(BaseModel):
    message: str

agent = Agent('openai:gpt-4o-mini', output_type=TestModel)

async def main():
    # We won't actually run it because we don't have a key, 
    # but we can check the class definition if needed or just guess.
    # Actually, let's just use python's dir() on a dummy object if possible.
    pass

if __name__ == "__main__":
    from pydantic_ai.agent import AgentRunResult
    print(dir(AgentRunResult))
