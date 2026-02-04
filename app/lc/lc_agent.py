import os
from langchain.chat_models import AzureChatOpenAI
from langchain.agents import create_openai_functions_agent
from lc_tools import get_dividend_tool

# LLM setup (modern LangChain)
llm = AzureChatOpenAI(
    deployment_name=os.environ["AZURE_OPENAI_DEPLOYMENT_NAME"],
    openai_api_key=os.environ["AZURE_OPENAI_API_KEY"],
    openai_api_base=os.environ["AZURE_OPENAI_API_BASE"],
    openai_api_version=os.environ.get("AZURE_OPENAI_API_VERSION", "2023-12-01"),
    temperature=0,
)

# Create a LangChain agent (modern API)
agent = create_openai_functions_agent(
    llm=llm,
    tools=[get_dividend_tool],
)

# Async run wrapper
async def run_agent(question: str) -> str:
    response = await agent.arun(question)
    return response
