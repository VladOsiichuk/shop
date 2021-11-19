from typing import Optional

from src.shop.orders.interfaces import (
    AddOrderLineUseCase,
    CheckoutOrderService,
    CheckoutOrderUseCase,
    CreateNewOrderUseCase,
    Order,
    OrderDoesNotExists,
    OrderLine,
)
from src.shop.products.interfaces import ProductDoesNotExists
from src.shop.uow import BaseUnitOfWork


class CreateNewOrderUseCaseImpl(CreateNewOrderUseCase):
    uow: BaseUnitOfWork

    def __init__(self, uow: BaseUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self) -> Order:
        order = Order()
        async with self.uow as uow:
            order = await uow.order_repo.persist(order)
            await uow.commit()
        return order


class CheckoutOrderUseCaseImpl(CheckoutOrderUseCase):
    uow: BaseUnitOfWork
    checkout_service: CheckoutOrderService

    def __init__(
        self, uow: BaseUnitOfWork, checkout_service: CheckoutOrderService
    ) -> None:
        self.uow = uow
        self.checkout_service = checkout_service

    async def __call__(self, *, order_id: int, receiver_phone_number: str) -> Order:
        async with self.uow as uow:
            order = await uow.order_repo.get(order_id)
            if not order:
                raise OrderDoesNotExists("Order does not exists!")
            order = await self.checkout_service.checkout(
                order=order, receiver_phone_number=receiver_phone_number
            )
            await uow.commit()
        return order


class AddOrderLineUseCaseImpl(AddOrderLineUseCase):
    uow: BaseUnitOfWork

    def __init__(self, uow: BaseUnitOfWork):
        self.uow = uow

    async def __call__(
        self, order_id: int, product_id: int, qty: Optional[int] = 1
    ) -> OrderLine:
        async with self.uow as uow:
            order = await uow.order_repo.get(order_id)
            if not order:
                raise OrderDoesNotExists("Order does not exists!")
            product = await uow.product_repo.get(product_id)
            if not product:
                raise ProductDoesNotExists("Product does not exists!")
            order_line = OrderLine(product_id=product_id, order_id=order_id, qty=qty)
            order_line = await uow.order_line_repo.persist(order_line)
            await uow.commit()
        return order_line
