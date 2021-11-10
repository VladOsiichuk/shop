from abc import ABCMeta, abstractmethod
from typing import Any


class BaseUnitOfWork(metaclass=ABCMeta):
    @abstractmethod
    def __enter__(self) -> "BaseUnitOfWork":
        """Start session."""

    async def __aexit__(self, *exc_info: Any) -> None:
        await self.rollback()

    @abstractmethod
    async def commit(self) -> None:
        """Persist changes."""

    @abstractmethod
    async def rollback(self) -> None:
        """Undo changes."""
