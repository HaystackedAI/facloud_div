# app/agents/langchain_agent.py
import os

from langchain_openai import ChatOpenAI
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain.agents import ChatPromptTemplate

from app.lc.lc_tools import add_numbers, get_server_time

# ---- LLM ----
llm = ChatOpenAI(
    model="gpt-5-mini",  # Azure DEPLOYMENT NAME
    base_url=f"{os.environ['AZURE_OPENAI_ENDPOINT'].rstrip('/')}/openai/v1/",
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

# ---- Tools ----
tools = [add_numbers, get_server_time]

# ---- Prompt ----
prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "You are a helpful AI agent. Use tools when appropriate."),
        ("human", "{input}"),
        ("placeholder", "{agent_scratchpad}"),
    ]
)

# ---- Agent ----
agent = create_tool_calling_agent(
    llm=llm,
    tools=tools,
    prompt=prompt,
)

agent_executor = AgentExecutor(
    agent=agent,
    tools=tools,
    verbose=True,   # IMPORTANT: shows tool calls in logs
)
