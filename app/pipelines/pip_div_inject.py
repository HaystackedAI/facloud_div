from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.service_div_inject import DivServicePg
from app.service.ser_dividend_finnhub import refresh_all_finnhub_market_data, refresh_finnhub_market_data
from app.db.repo.repo_div_inject import DividendRepo

class DivPipeline:


    @staticmethod
    async def run_hourly(db: AsyncSession) -> dict:
        enriched = refresh_all_finnhub_market_data()
        # pruned = await DivServicePg.pruen_marketcap_anomalies(db)

        return {
            # "deleted_past": deleted,
            # "upserted": upserted,
            "enriched": enriched,
            # "Anomaly": pruned,
        }




    @staticmethod
    async def run_daily(db: AsyncSession, today: date) -> dict:
        deleted  = await DivServicePg.delete_past(db, today)
        upserted = await DivServicePg.from_nasdaq_2pg_4wk(db, today)
        pruned_non_stock = await DivServicePg.prune_non_stock_type(db)  
        # enriched = refresh_all_finnhub_market_data()
        # pruned = await DivServicePg.prune_marketcap_anomalies(db)

        return {
            "deleted_past": deleted,
            "upserted": upserted,
            # "enriched": enriched,
            # "Anomaly": pruned,
        }


    @staticmethod
    async def run_monthly(db: AsyncSession) -> dict:
        repo = DividendRepo(db)
        # upserted = await DivServicePg.from_google_to_pg(db)   #step 1. 
        sync_type = await repo.sync_div_type_from_symbols()   #step 2.
        # pruned = await DivServicePg.pruen_marketcap_anomalies(db)

        return {
            "upserted": "upserted",
        }



    @staticmethod
    async def run_yearly(db: AsyncSession) -> dict:
        # save2csv = await grab_symbol_list_form_finnhub_to_csv()
        # csv2pg = await DividendRepo(db).finnhub_symbol_upsert_loop_csv()
        
        return {
            "upserted": "upserted",
        }

