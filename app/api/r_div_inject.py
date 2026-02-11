# app/api/routes/wage.py
from datetime import date
from fastapi import APIRouter, Depends, HTTPException, Path, UploadFile, File, Query
from fastapi import BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.db_async import get_db
from app.util.util_grab_div import grab_symbol_list_form_finnhub_to_csv
from app.service.ser_dividend_finnhub import refresh_all_finnhub_market_data, refresh_finnhub_market_data
from app.pipelines.pip_div_inject import DivPipeline
from app.db.repo.repo_div_inject import DividendRepo
# from app.service.ser_az_data_lake import list_files, write_json


injRou = APIRouter()


@injRou.post("/div_hourlyrun", summary="Fetch hourly dividend data")
async def run_hourly_pipeline(background_tasks: BackgroundTasks):
    background_tasks.add_task(DivPipeline.run_hourly)
    return {"status": "started", "message": "Hourly dividend pipeline started in background"}   



@injRou.post("/div_dailyrun", summary="Fetch daily dividend data")
async def run_daily_pipeline(
    db: AsyncSession = Depends(get_db),
):
    return await DivPipeline.run_daily(db, date.today())


@injRou.post("/div_dailyrun_background", summary="Fetch daily dividend data in background")
async def run_daily_pipeline_background(    run_background_tasks: BackgroundTasks,):
    run_background_tasks.add_task(DivPipeline.run_daily_background, date.today())
    return {"status": "started", "message": "Daily dividend pipeline started in background"}



@injRou.post("/div_monthly_google_sheet")
async def monthly_read_from_google_sheet(
    db: AsyncSession = Depends(get_db),
):
    return await DivPipeline.run_monthly(db)


@injRou.post("/div_yearly_symbol_list")
async def yearly_exchange_list(
    db: AsyncSession = Depends(get_db),
):
    return await DivPipeline.run_yearly(db)



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




