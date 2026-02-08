# app/service/ser_dividend_load.py
import csv, pandas as pd
from datetime import datetime, date
from datetime import date, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import delete

from app.db.models.m_div import Div  # your ORM model
from app.service.ser_div_pg_load2pg import DivDfLoader
from app.util.util_grab_div import grab_nasdaq_to_df, grab_googlesheet_to_df

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
    async def from_nasdaq_2pg_4wk(db: AsyncSession, today: date) -> int:
        total = 0
        start = today
        weeks = 4
        end = start + timedelta(weeks = weeks)

        cur = start
        print("start:", start, "end:", end)
        while cur <= end:
            try:
                df = grab_nasdaq_to_df(target_date=cur.strftime("%Y-%m-%d"))
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

    
    @staticmethod
    def _from_google_to_df(df: pd.DataFrame) -> pd.DataFrame:
        df = df.copy()

        # extract symbol from "Company (XXX)"
        df["symbol"] = df["Company"].apply(
            lambda x: x.split("(")[-1].replace(")", "").strip()
            if isinstance(x, str) and "(" in x and ")" in x
            else None
        )

        return pd.DataFrame({
            "company_name": df["Company"],
            "symbol": df["symbol"],
            "dividend_ex_date": pd.to_datetime(df["Ex-Dividend Date"], errors="coerce").dt.date,
            "payment_date": pd.to_datetime(df["Payment Date"], errors="coerce").dt.date,
            "dividend_rate": pd.to_numeric(df["Dividend"], errors="coerce"),
            "yield_percent": (
                df["Yield"]
                .astype(str)
                .str.rstrip("%")
                .pipe(pd.to_numeric, errors="coerce")
            ),
            # fields Google doesn't have
            "record_date": None,
            "indicated_annual_dividend": None,
            "announcement_date": None,
            "latest_price": None,
            "market_cap": None,
        })
    

    @staticmethod
    async def from_google_to_pg(db: AsyncSession) -> int:
        df_raw = grab_googlesheet_to_df()

        if df_raw is None or df_raw.empty:
            return 0

        df = DivServicePg._from_google_to_df(df_raw)

        return await DivDfLoader.upsert_df_symbol_only(db, df)