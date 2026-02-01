# app/service/ser_dividend_load.py
import csv, pandas as pd
from datetime import datetime, date
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import delete

from app.db.models.m_div import Div  # your ORM model
from app.service.ser_div_pg_load2pg import DivDfLoader
from app.service.ser_div_pg_grab_nasdaq import grab_dividends_to_df

DATE_FMT = "%m/%d/%Y"  # Nasdaq CSV date format


class DivServicePg:

    @staticmethod
    async def delete_past(db: AsyncSession, today: date) -> int:
        stmt = delete(Div).where(Div.dividend_ex_date < today)
        result = await db.execute(stmt)
        await db.commit()
        return result.closed


    @staticmethod
    async def pruen_marketcap_anomalies(db: AsyncSession) -> int:
        MIN_MARKETCAP = 1_000        # 1B
        MAX_MARKETCAP = 5_000_000    # 5T

        stmt = delete(Div).where(
            (Div.market_cap < MIN_MARKETCAP) |
            (Div.market_cap > MAX_MARKETCAP) |
            (Div.market_cap.is_(None))
        )

        result = await db.execute(stmt)
        await db.commit()
        return result.closed

    @staticmethod
    async def grab_from_nasdaq_2pg_4wk(db: AsyncSession, today: date) -> int:
        """
        Grab dividends from today -> next 4 weeks and upsert into PostgreSQL.

        Returns:
            Number of rows inserted/updated
        """
        total = 0
        start = today
        end = start + timedelta(weeks=1)

        cur = start
        print("start:", start, "end:", end)
        while cur <= end:
            try:
                df = grab_dividends_to_df(target_date=cur.strftime("%Y-%m-%d"))
                print(cur, "df.shape:", None if df is None else df.shape)

                if df is None or df.empty:
                    cur += timedelta(days=1)
                    continue

                total += await DivDfLoader.upsert_df_symbol_only(db, df)

            except Exception as e:
                # Ignore weekends/holidays / empty responses
                pass

            cur += timedelta(days=1)

        return total
