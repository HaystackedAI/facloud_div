from langchain.tools import Tool
from app.agent.age_tools import get_dividend_data_tool, search_web_tool  # your existing functions

# Wrap your existing functions as LangChain Tools
get_dividend_tool = Tool(
    name="get_dividend_data",
    func=get_dividend_data_tool,
    description="Fetch dividend data for a given ticker."
)

search_web_tool = Tool(
    name="search_web",
    func=search_web_tool,
    description="Search the web for relevant financial info."
)


def echo_tool(input_text: str) -> str:
    return f"Echo: {input_text}"