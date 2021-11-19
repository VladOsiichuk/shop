from typing import Any

from src.shop.orders.interfaces import OrderLineRepository, OrderRepository
from src.shop.products.interfaces import ProductRepository
from src.shop.uow import BaseUnitOfWork


class DummyUnitOfWork(BaseUnitOfWork):
    def __init__(
        self,
        product_repo: ProductRepository,
        order_repo: OrderRepository,
        order_line_repo: OrderLineRepository,
    ) -> None:
        self.product_repo = product_repo
        self.order_repo = order_repo
        self.order_line_repo = order_line_repo

    async def __aenter__(self) -> BaseUnitOfWork:
        return self

    async def __aexit__(self, *exc_info: Any) -> None:
        pass

    async def commit(self) -> None:
        pass

    async def rollback(self) -> None:
        pass
