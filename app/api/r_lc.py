# app/api/lc_routes.py
from fastapi import APIRouter

# from app.lc.lc_agent import run_lc_agent
from app.schemas.sch_lc import QueryRequest, QueryResponse
from app.core.lc_az_openai import run_chain

lcRou = APIRouter()


@lcRou.post("/lc_query1", response_model=QueryResponse)
async def lc_query(req: QueryRequest):
    answer = await run_chain(req.question)
    return QueryResponse(answer=answer)




@lcRou.post("/langchain/lc_query", response_model=QueryResponse)
async def lc1_query(question: str):
    answer = await run_chain(question)
    return {"answer": answer}