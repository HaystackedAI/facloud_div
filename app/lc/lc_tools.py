# app/langchain/tools.py
from langchain.tools import tool
import anyio
from app.agent.age_tools import (
    get_dividend_data_tool,
    search_web_tool,
)

@tool
def get_dividend_data(query: str) -> dict:
    """Internal dividend database: yield, payout ratio, history."""
    return anyio.from_thread.run(get_dividend_data_tool, query)


@tool
def search_web(query: str) -> dict:
    """Live web search for recent news and sentiment."""
    return anyio.from_thread.run(search_web_tool, query)


TOOLS = [get_dividend_data, search_web]
