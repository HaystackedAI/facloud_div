# app/api/routes/wage.py
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile, File, Query
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_async import get_db

from app.service.ser_dividend_finnhub import refresh_all_finnhub_market_data, refresh_finnhub_market_data
from app.service.ser_div_pg_grab_nasdaq import grab_dividends_to_csv
from app.service.ser_div_pipeline import DivPipeline

injRou = APIRouter()


@injRou.post("/div_dailyrun", summary="Fetch daily dividend data")
async def run_daily_pipeline(
    db: AsyncSession = Depends(get_db),
):
    return await DivPipeline.run_daily(db, date.today())


# @injRou.post("/grab-finnhub/{symbol}")
# def grab_finnhub(symbol: str):
#     try:
#         return refresh_finnhub_market_data(symbol)
#     except LookupError as e:
#         raise HTTPException(status_code=404, detail=str(e))
#     except ValueError as e:
#         raise HTTPException(status_code=502, detail=str(e))


@injRou.post("/finnhub-update-price", summary="Update price once per hour. ")
def update_all_finnhub():
    try:
        return refresh_all_finnhub_market_data()

    except ValueError as e:
        raise HTTPException(status_code=502, detail=str(e))


@injRou.post("/finnhub-background")
def update_all_finnhub_bg(background_tasks: BackgroundTasks):
    background_tasks.add_task(refresh_all_finnhub_market_data)
    return {
        "status": "started",
        "message": "Finnhub refresh job started in background"
    }


