# app/service/ser_dividend_grab.py
import requests
import pandas as pd
from sqlalchemy.ext.asyncio import AsyncSession

from app.service.ser_dividend_load import DivDfLoader
from app.service.ser_dividend_grab_nasdaq import grab_dividends_to_df


class DividendPipeline:

    @staticmethod
    async def nasdaq2pg(db: AsyncSession, target_date: str) -> int:
        """
        Grab dividends from Nasdaq for the target date and load into PostgreSQL.

        Returns:
            Number of rows inserted
        """
        # Step 1: Grab dividends and save to CSV
        df = grab_dividends_to_df(target_date=target_date)

        # Step 3: Load DataFrame into PostgreSQL
        inserted_count = await DivDfLoader.load_df(db, df)

        return inserted_count