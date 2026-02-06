# app/api/routes/wage.py
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile, File, Query
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_async import get_db

from app.service.ser_dividend_finnhub import refresh_all_finnhub_market_data, refresh_finnhub_market_data
from app.service.ser_div_pg_grab_nasdaq import grab_dividends_to_csv
from app.pipelines.pip_div_inject import DivPipeline
from app.service.ser_az_data_lake import list_files, write_json

from app.service.ser_div_pg_load2pg import upsert_dividends

injRou = APIRouter()


@injRou.post("/div_dailyrun", summary="Fetch daily dividend data")
async def run_daily_pipeline(
    db: AsyncSession = Depends(get_db),
):
    return await DivPipeline.run_daily(db, date.today())


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


@injRou.post("/write_to_lake")
def write_to_lake(payload: dict):
    file_path = write_json(payload)
    return {"status": "success", "file": file_path}


@injRou.post("/read_from_google_sheet")
async def read_from_google_sheet(db: AsyncSession = Depends(get_db),
                                 ):
    import pandas as pd
    url = "https://docs.google.com/spreadsheets/d/15QBf76ab4zSt-S-oGSrSpgdJngpdGCxFMJqZkC6_sAM/export?format=csv"
    df = pd.read_csv(url).dropna(how='all').reset_index(drop=True)

    # Upsert into database
    total = await upsert_dividends(db, df)
    return {"inserted_or_updated": total}

    # url = "https://docs.google.com/spreadsheets/d/15QBf76ab4zSt-S-oGSrSpgdJngpdGCxFMJqZkC6_sAM/export?format=csv"
    # df = pd.read_csv(url)
    # df = df.dropna(how='all')
    # df = df.reset_index(drop=True)
    # # Convert NaN to None (JSON-safe)
    # print(df.head)

    # return {"status": "success",}
