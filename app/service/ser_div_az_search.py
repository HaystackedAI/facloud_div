# app/services/search_service.py
from app.integrations.azure_ai_search import search_client
from app.integrations.azure_openai_embedder import embed_fn_azure_new_v1

async def search_dividends(query: str, top_k: int):
    query_vec = await embed_fn_azure_new_v1(query)

    results = search_client.search(
        search_text=query,
        vector_queries=[{
            "vector": query_vec,
            "k": 50,
            "fields": "embedding",
        }],
        top=top_k,
    )

    out = []
    async for r in results:
        out.append({
            "id": r["id"],
            "pg_id": r["pg_id"],
            "content": r["chunk_text"],
            "score": r["@search.score"],
        })
    return out
