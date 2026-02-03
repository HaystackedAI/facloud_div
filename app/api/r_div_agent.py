from fastapi import APIRouter
from app.service.ser_ai_rag import rag_query_contract, rag_query
from app.agent.ag_core import run_agent

agentRou = APIRouter(prefix="/rag", tags=["RAG"])



@agentRou.post("/query")
async def query_rag(payload: dict):
    question = payload["question"]
    top_k = payload.get("top_k", 5)
    return await rag_query(question, top_k)


@agentRou.post("/ag_query")
async def agent_query(q: str):
    return await run_agent(q)