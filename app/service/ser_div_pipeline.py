from datetime import date
from sqlalchemy.ext.asyncio import AsyncSession
from app.service.ser_div_pg import DivServicePg

class DividendPipeline:

    @staticmethod
    async def run_daily(db: AsyncSession, today: date) -> dict:
        deleted  = await DivServicePg.delete_past(db, today)
        upserted = await DivServicePg.upsert_today_and_future(db, today)

        enriched = await DividendService.enrich_price_marketcap(db)

        filtered = await DividendService.delete_below_marketcap(
            db, min_marketcap=1_000_000_000
        )

        return {
            "deleted_past": deleted,
            "upserted": upserted,
            "enriched": enriched,
            "filtered": filtered,
        }
