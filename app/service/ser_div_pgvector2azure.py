# app/services/indexing_service.py
from app.db.repo.repo_div_pgvector import f

BATCH_SIZE = 500

async def bulk_index_dividends(db_session):
    chunks = await fetch_chunks(db_session)

    batch = []
    for c in chunks:
        batch.append({
            "id": str(c.id),
            "pg_id": str(c.div_id),
            "chunk_text": c.content,
            "embedding": c.embedding,
        })

        if len(batch) >= BATCH_SIZE:
            await search_client.upload_documents(batch)
            batch.clear()

    if batch:
        await search_client.upload_documents(batch)
