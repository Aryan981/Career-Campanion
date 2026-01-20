import asyncio
from pydantic_ai import Agent
from pydantic import BaseModel
from pydantic_ai.models.test import TestModel

class Success(BaseModel):
    x: int

# Use TestModel to avoid API calls
agent = Agent(TestModel(), output_type=Success)

async def main():
    result = await agent.run("hello")
    print(f"Result type: {type(result)}")
    print(f"Result dir: {dir(result)}")
    if hasattr(result, 'data'):
        print(f"Result data: {result.data}")
    else:
        print("RESULT HAS NO DATA")
    
    if hasattr(result, 'output'):
        print(f"Result output type: {type(result.output)}")
        print(f"Result output: {result.output}")

async def main_wrapper():
    await main()

if __name__ == "__main__":
    asyncio.run(main_wrapper())
