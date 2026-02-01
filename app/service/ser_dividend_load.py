# app/service/ser_dividend_load.py
import csv, pandas as pd
from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.dialects.postgresql import insert

from app.db.models.m_div import Div  # your ORM model

DATE_FMT = "%m/%d/%Y"  # Nasdaq CSV date format


class DividendCsvLoader:

    @staticmethod
    async def load_csv(db: AsyncSession, filename: str) -> int:
        """
        Read a CSV (normalized) and insert into DB.

        Returns:
            Number of rows inserted
        """
        inserted = 0
        file_path = f"data/dividends/{filename}"

        with open(file_path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)

            for row in reader:
                dividend = Div(
                    company_name=row["companyName"],
                    symbol=row["symbol"],
                    dividend_ex_date=datetime.strptime(row["dividend_Ex_Date"], DATE_FMT).date(),
                    payment_date=datetime.strptime(row["payment_Date"], DATE_FMT).date(),
                    record_date=datetime.strptime(row["record_Date"], DATE_FMT).date(),
                    dividend_rate=float(row["dividend_Rate"]),
                    indicated_annual_dividend=float(row["indicated_Annual_Dividend"]),
                    announcement_date=datetime.strptime(row["announcement_Date"], DATE_FMT).date(),
                )

                db.add(dividend)
                inserted += 1

        await db.commit()
        return inserted




class DivDfLoader:

    @staticmethod
    async def load_df(db: AsyncSession, df: pd.DataFrame) -> int:
        """
        Read a DataFrame and insert into DB.

        Returns:
            Number of rows inserted
        """
        inserted = 0

        for _, row in df.iterrows():
            dividend = Div(
                company_name=row["companyName"],
                symbol=row["symbol"],
                dividend_ex_date=datetime.strptime(row["dividend_Ex_Date"], DATE_FMT).date(),
                payment_date=datetime.strptime(row["payment_Date"], DATE_FMT).date(),
                record_date=datetime.strptime(row["record_Date"], DATE_FMT).date(),
                dividend_rate=float(row["dividend_Rate"]),
                indicated_annual_dividend=float(row["indicated_Annual_Dividend"]),
                announcement_date=datetime.strptime(row["announcement_Date"], DATE_FMT).date(),
            )

            db.add(dividend)
            inserted += 1

        await db.commit()
        return inserted



    @staticmethod
    async def upsert_df_symbol_only(db: AsyncSession, df: pd.DataFrame) -> int:
        rows = []

        for _, row in df.iterrows():
            rows.append({
                "company_name": row["companyName"],
                "symbol": row["symbol"],
                "dividend_ex_date": datetime.strptime(row["dividend_Ex_Date"], DATE_FMT).date(),
                "record_date": datetime.strptime(row["record_Date"], DATE_FMT).date(),
                "payment_date": datetime.strptime(row["payment_Date"], DATE_FMT).date(),
                "dividend_rate": float(row["dividend_Rate"]),
                "indicated_annual_dividend": float(row["indicated_Annual_Dividend"]),
                "announcement_date": datetime.strptime(row["announcement_Date"], DATE_FMT).date(),
            })

        if not rows:
            return 0

        stmt = insert(Div).values(rows) 

        stmt = stmt.on_conflict_do_update(
            index_elements=["symbol"],
            set_={
                "company_name": stmt.excluded.company_name,
                "dividend_ex_date": stmt.excluded.dividend_ex_date,
                "record_date": stmt.excluded.record_date,
                "payment_date": stmt.excluded.payment_date,
                "dividend_rate": stmt.excluded.dividend_rate,
                "indicated_annual_dividend": stmt.excluded.indicated_annual_dividend,
                "announcement_date": stmt.excluded.announcement_date,
                "updated_at": datetime.utcnow(),
            },
        )

        res = await db.execute(stmt)
        await db.commit()
        return len(rows)