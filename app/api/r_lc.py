# main.py
import os
from fastapi import APIRouter
from pydantic import BaseModel

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage

lcRou = APIRouter()

# ---- LLM (Azure OpenAI via LangChain) ----
llm = ChatOpenAI(
    model="gpt-5-nano",  # Azure DEPLOYMENT NAME
    base_url="https://haystacked.cognitiveservices.azure.com/openai/v1/",
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
)

# ---- Request schema ----
class ChatRequest(BaseModel):
    message: str

# ---- Agent endpoint ----
@lcRou.post("/agent/chat")
async def chat_agent(req: ChatRequest):
    messages = [
        SystemMessage(content="You are a helpful AI agent."),
        HumanMessage(content=req.message),
    ]

    response = llm.invoke(messages)

    return {
        "reply": response.content
    }
