import asyncio
from pydantic_ai import Agent

agent = Agent('openai:gpt-4o-mini')

async def main():
    try:
        # We don't have a key, but we can see the signature and type
        # signature of run
        import inspect
        print(f"run signature: {inspect.signature(agent.run)}")
        
        # Check what the return class is
        from pydantic_ai.result import RunResult
        print(f"RunResult attributes: {dir(RunResult)}")
        
    except Exception as e:
        print(f"Error: {e}")

asyncio.run(main())
