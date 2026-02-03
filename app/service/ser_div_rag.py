from app.service.ser_div_az_search import search_dividends
from app.core.rag_prompt import SYSTEM_PROMPT, build_user_prompt
from app.core.azure_openai_chat import chat_completion

async def rag_query(question: str, top_k: int):
    chunks = await search_dividends(question, top_k)

    if not chunks:
        return {
            "answer": "I don't have enough dividend data to answer this question.",
            "sources": [],
            "meta": {"retrieved_chunks": 0},
        }

    contexts = [c["content"] for c in chunks]

    user_prompt = build_user_prompt(question, contexts)
    answer = await chat_completion(SYSTEM_PROMPT, user_prompt)

    return {
        "answer": answer,
        "sources": chunks,
        "meta": {
            "retrieved_chunks": len(chunks),
        },
    }
