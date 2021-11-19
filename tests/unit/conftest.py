import pytest

from src.shop.orders.memory import MemoryOrderLineRepository, MemoryOrderRepository
from src.shop.products.memory import MemoryProductRepository
from src.shop.testing import DummyUnitOfWork


@pytest.fixture
def product_repo() -> MemoryProductRepository:
    return MemoryProductRepository()


@pytest.fixture
def order_repo() -> MemoryOrderRepository:
    return MemoryOrderRepository()


@pytest.fixture
def order_line_repo() -> MemoryOrderLineRepository:
    return MemoryOrderLineRepository()


@pytest.fixture
def uow(product_repo, order_repo, order_line_repo) -> DummyUnitOfWork:
    return DummyUnitOfWork(
        product_repo=product_repo,
        order_repo=order_repo,
        order_line_repo=order_line_repo,
    )
