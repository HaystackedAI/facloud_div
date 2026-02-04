# app/langchain/agent.py
from langchain.agents import create_agent
from langchain.agents.structured_output import ToolStrategy
from app.core.lc_az_openai import llm
from app.schemas.sch_lc import AgentResponse
from .lc_tools import TOOLS

agent = create_agent(
    model=llm,
    tools=TOOLS,
    response_format=ToolStrategy(schema=AgentResponse)
)
