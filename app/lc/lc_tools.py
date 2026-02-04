# app/agents/tools.py
from langchain.tools import tool
from datetime import datetime

@tool
def add_numbers(a: int, b: int) -> int:
    """Add two integers and return the result."""
    return a + b


@tool
def get_server_time() -> str:
    """Return the current server time as ISO string."""
    return datetime.utcnow().isoformat()
