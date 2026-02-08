from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.service_div_inject import DivServicePg
from app.service.ser_dividend_finnhub import refresh_all_finnhub_market_data, refresh_finnhub_market_data

class DivPipeline:

    @staticmethod
    async def run_daily(db: AsyncSession, today: date) -> dict:
        deleted  = await DivServicePg.delete_past(db, today)
        upserted = await DivServicePg.from_nasdaq_2pg_4wk(db, today)
        enriched = refresh_all_finnhub_market_data()
        pruned = await DivServicePg.pruen_marketcap_anomalies(db)

        return {
            "deleted_past": deleted,
            "upserted": upserted,
            "enriched": enriched,
            "Anomaly": pruned,
        }


    @staticmethod
    async def run_monthly(db: AsyncSession) -> dict:
        upserted = await DivServicePg.from_google_to_pg(db)
        # enriched = refresh_all_finnhub_market_data()
        # pruned = await DivServicePg.pruen_marketcap_anomalies(db)

        return {
            "upserted": upserted,
        }
