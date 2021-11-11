from abc import ABCMeta, abstractmethod

from src.shop.orders.interfaces import OrderRepository, OrderLineRepository
from src.shop.products.interfaces import ProductRepository
from typing import Any


class BaseUnitOfWork(metaclass=ABCMeta):
    product_repo: ProductRepository
    order_repo: OrderRepository
    order_line_repo: OrderLineRepository

    @abstractmethod
    async def __aenter__(self) -> "BaseUnitOfWork":
        """Start session."""

    async def __aexit__(self, *exc_info: Any) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        """Persist changes."""

    @abstractmethod
    async def rollback(self) -> None:
        """Undo changes."""
