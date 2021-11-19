import pytest

from src.shop.orders.interfaces import Order
from src.shop.orders.memory import MemoryOrderRepository


@pytest.fixture
async def order_in_repo(order_repo: MemoryOrderRepository):
    order = Order(status="new")
    return await order_repo.persist(order)


async def test_persist(order_repo: MemoryOrderRepository):
    order = await order_repo.persist(Order())
    assert isinstance(order, Order)
    assert order.id

    another_order = await order_repo.persist(Order())
    assert isinstance(another_order, Order)
    assert another_order.id

    assert another_order != order


async def test_get(order_repo: MemoryOrderRepository, order_in_repo: Order):
    assert order_in_repo == await order_repo.get(order_in_repo.id)


async def test_get_order_not_exists(order_repo: MemoryOrderRepository):
    assert await order_repo.get(1) is None
