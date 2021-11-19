from typing import Any, Optional, Protocol

from sqlalchemy.ext.asyncio.session import AsyncSession

from src.shop.orders.database import (
    DatabaseOrderLineRepository,
    DatabaseOrderRepository,
)
from src.shop.products.database import DatabaseProductRepository
from src.shop.uow import BaseUnitOfWork


class SessionFactory(Protocol):
    def __call__(self) -> AsyncSession:
        """Create a session"""


class SQLAlchemyUnitOfWork(BaseUnitOfWork):
    _session: Optional[AsyncSession]
    _session_factory: SessionFactory

    def __init__(self, session_factory: SessionFactory):
        self._session = None
        self._session_factory = session_factory

    async def __aenter__(self) -> "SQLAlchemyUnitOfWork":
        if self._session is not None:
            raise RuntimeError("UoW is already working")

        self._session = session = self._session_factory()
        self.product_repo = DatabaseProductRepository(self._session)
        self.order_repo = DatabaseOrderRepository(self._session)
        self.order_line_repo = DatabaseOrderLineRepository(self._session)
        await session.__aenter__()

        return self

    async def __aexit__(self, *exc_info: Any):
        assert self._session is not None

        await super().__aexit__(*exc_info)
        await self._session.__aexit__(*exc_info)

        self._session = None

    async def commit(self) -> None:
        assert self._session is not None

        await self._session.commit()

    async def rollback(self) -> None:
        assert self._session is not None

        await self._session.rollback()
