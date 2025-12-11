from typing import Callable, Dict, Any
import inspect
import asyncio

tool_registry: Dict[str, Callable[..., Any]] = {}

def register_tool(name: str):
    def decorator(func: Callable[..., Any]):
        tool_registry[name] = func
        return func
    return decorator

async def call_tool(name: str, state: dict, **kwargs) -> Any:
    if name not in tool_registry:
        raise ValueError(f"Tool '{name}' is not registered.")
    
    func = tool_registry[name]
    
    if inspect.iscoroutinefunction(func):
        return await func(state, **kwargs)
    else:
        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(None, lambda: func(state, **kwargs))
