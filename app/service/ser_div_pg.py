# app/service/ser_dividend_load.py
import csv, pandas as pd
from datetime import datetime, date
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import delete

from app.db.models.m_div import Div  # your ORM model

DATE_FMT = "%m/%d/%Y"  # Nasdaq CSV date format


class DivServicePg:

    @staticmethod
    async def delete_past(db: AsyncSession, today: date) -> int:
        stmt = delete(Div).where(Div.dividend_ex_date < today)
        result = await db.execute(stmt)
        await db.commit()
        return result.closed



    @staticmethod
    async def upsert_today_and_future(
        db: AsyncSession,
        df: pd.DataFrame,
    ) -> int:
        if df is None or df.empty:
            return 0

        rows = [
            {
                "company_name": r["companyName"],
                "symbol": r["symbol"],
                "dividend_ex_date": datetime.strptime(r["dividend_Ex_Date"], DATE_FMT).date(),
                "record_date": datetime.strptime(r["record_Date"], DATE_FMT).date(),
                "payment_date": datetime.strptime(r["payment_Date"], DATE_FMT).date(),
                "dividend_rate": float(r["dividend_Rate"]),
                "indicated_annual_dividend": float(r["indicated_Annual_Dividend"]),
                "announcement_date": datetime.strptime(r["announcement_Date"], DATE_FMT).date(),
            }
            for r in df.to_dict(orient="records")
        ]

        stmt = insert(Div).values(rows)

        stmt = stmt.on_conflict_do_update(
            index_elements=["symbol"],  # symbol-only uniqueness
            set_={
                "company_name": stmt.excluded.company_name,
                "dividend_ex_date": stmt.excluded.dividend_ex_date,
                "record_date": stmt.excluded.record_date,
                "payment_date": stmt.excluded.payment_date,
                "dividend_rate": stmt.excluded.dividend_rate,
                "indicated_annual_dividend": stmt.excluded.indicated_annual_dividend,
                "announcement_date": stmt.excluded.announcement_date,
            },
        )

        await db.execute(stmt)
        await db.commit()
        return len(rows)
    


    
