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


from langchain.tools import tool

@tool
def search_database(query: str, limit: int = 10) -> str:
    """Search the customer database for records matching the query.

    Args:
        query: Search terms to look for
        limit: Maximum number of results to return
    """
    return f"Found {limit} results for '{query}'"