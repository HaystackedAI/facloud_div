from fastapi import APIRouter
from app.service.ser_div_rag import rag_query

ragContractRou = APIRouter(prefix="/rag", tags=["RAG"])

@ragContractRou.post("/query")
async def query_rag(payload: dict):
    question = payload["question"]
    top_k = payload.get("top_k", 5)
    return await rag_query(question, top_k)
