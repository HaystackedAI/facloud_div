from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse

from app.api.r_div_inject import injRou
from app.api.r_div_show import divRou
from app.api.r_div_embedding import divEmbedding

rou = APIRouter()

rou.include_router(divRou, prefix="/div_show", tags=["show PG, pgvector, Datalake, Azure Congnitive Search"])
rou.include_router(injRou, prefix="/div_inject", tags=["From Nasdaq to Postgres to Datalake"])


rou.include_router(divEmbedding, prefix="/divrag", tags=["Embedding"])




@rou.get("/")
def rouGet():
    return RedirectResponse(url="https://ainvoaice.com")
