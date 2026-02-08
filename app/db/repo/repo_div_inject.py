# app/repositories/dividend_repo.py
from decimal import Decimal
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.engine import Result
from sqlalchemy.dialects.postgresql import insert

from app.db.models.m_div import Div


class DividendRepo:
    def __init__(self, db: AsyncSession):
        self.db = db

    # -------------------------
    # Query Methods
    # -------------------------
    async def get_by_symbol(self, symbol: str) -> List[Div]:
        """Return all Div rows for a given symbol."""
        result = await self.db.execute(
            select(Div).where(Div.symbol == symbol)
        )
        return list(result.scalars().all())

    async def get_all(self) -> List[Div]:
        """Return all Div rows."""
        result = await self.db.execute(select(Div))
        return list(result.scalars().all())

    # -------------------------
    # Update / Modify Methods
    # -------------------------
    async def update_market_data(
        self,
        rows: List[Div],
        latest_price: Decimal,
        market_cap: Decimal,
        commit: bool = False,
    ) -> int:
        """
        Update latest_price, market_cap, and recompute yield_percent.
        If commit=True, commits automatically.
        Returns the number of rows updated.
        """
        updated = 0
        for row in rows:
            row.latest_price = latest_price
            row.market_cap = market_cap
            if row.indicated_annual_dividend and latest_price > 0:
                row.yield_percent = (
                    Decimal(row.indicated_annual_dividend) / latest_price * Decimal("100")
                )
            updated += 1

        if commit:
            await self.db.commit()

        return updated

    # -------------------------
    # Bulk Upsert Example
    # -------------------------
    async def google_bulk_upsert(self, records: list[dict], conflict_keys: list[str]) -> int:
        if not records:
            return 0

        stmt = insert(Div).values(records)
        # Update only columns in records, skip conflict keys
        update_cols = {k: stmt.excluded[k] for k in records[0].keys() if k not in conflict_keys}
        stmt = stmt.on_conflict_do_update(index_elements=conflict_keys, set_=update_cols)

        result: Result = await self.db.execute(stmt)
        await self.db.commit()

        # Runtime-safe rowcount
        return getattr(result, "rowcount", 0)
