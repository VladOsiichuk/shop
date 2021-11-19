from typing import List, Optional

from src.shop.orders.interfaces import (
    Order,
    OrderLine,
    OrderLineRepository,
    OrderRepository,
)


class MemoryOrderRepository(OrderRepository):
    _db: dict[int, Order]
    _id_counter: int

    def __init__(self):
        self._id_counter = 1
        self._db = {}

    async def get(self, order_id: int) -> Optional[Order]:
        return self._db.get(order_id)

    async def persist(self, order: Order) -> Order:
        order.id = self._id_counter
        self._db[self._id_counter] = order
        self._id_counter += 1
        return order


class MemoryOrderLineRepository(OrderLineRepository):
    _db: dict[int, OrderLine]
    _id_counter: int

    def __init__(self):
        self._id_counter = 1
        self._db = {}

    async def get_by_order_id(self, order_id: int) -> List[OrderLine]:
        return [row for row in self._db.values() if row.order_id == order_id]

    async def persist(self, order_line: OrderLine) -> OrderLine:
        order_line.id = self._id_counter
        self._db[self._id_counter] = order_line
        self._id_counter += 1
        return order_line
