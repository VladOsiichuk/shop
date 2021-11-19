from typing import List, Optional

import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship

from src.shop.db import Base
from src.shop.orders.interfaces import Order as DomainOrder
from src.shop.orders.interfaces import OrderLine as DomainOrderLine
from src.shop.orders.interfaces import OrderLineRepository, OrderRepository


class Order(Base):
    __tablename__ = "orders"

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    status = sa.Column(sa.String(length=64), default="new")
    receiver_phone_number = sa.Column(sa.String(length=12), nullable=True, default=None)


class OrderLine(Base):
    __tablename__ = "order_lines"

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    order_id = sa.Column(sa.BigInteger, sa.ForeignKey("orders.id"))
    order = relationship("Order", primaryjoin="OrderLine.order_id == Order.id")

    product_id = sa.Column(sa.BigInteger, sa.ForeignKey("products.id"))
    product = relationship("Product", primaryjoin="OrderLine.product_id == Product.id")

    qty = sa.Column(sa.Integer, default=1)


class DatabaseOrderRepository(OrderRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.db = session

    async def get(self, order_id: int) -> Optional[DomainOrder]:
        query = sa.select(Order).where(Order.id == order_id)
        order = (await self.db.execute(query)).scalars().one_or_none()
        if not order:
            return None
        return DomainOrder.from_orm(order)

    async def persist(self, order: DomainOrder) -> DomainOrder:
        data = order.dict(exclude_unset=True)
        if order.id:
            order_id = data.pop("id")
            query = (
                sa.update(Order)
                .values(**data)
                .where(Order.id == order_id)
                .returning(Order)
            )
        else:
            query = sa.insert(Order).values(**data).returning(Order)

        db_object = (await self.db.execute(query)).fetchone()
        return DomainOrder.from_orm(db_object)


class DatabaseOrderLineRepository(OrderLineRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.db = session

    async def get_by_order_id(self, order_id: int) -> List[DomainOrderLine]:
        query = sa.select(OrderLine).where(OrderLine.order_id == order_id)
        order_lines = (await self.db.execute(query)).scalars().all()
        return list(map(DomainOrderLine.from_orm, order_lines))

    async def persist(self, order_line: DomainOrderLine) -> DomainOrderLine:
        data = order_line.dict(exclude_unset=True)
        if order_line.id:
            order_id = data.pop("id")
            query = (
                sa.update(OrderLine)
                .values(**data)
                .where(Order.id == order_id)
                .returning(OrderLine)
            )
        else:
            query = sa.insert(OrderLine).values(**data).returning(OrderLine)

        db_object = (await self.db.execute(query)).fetchone()
        return DomainOrderLine.from_orm(db_object)
