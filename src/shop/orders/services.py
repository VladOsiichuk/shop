from src.shop.orders.interfaces import CheckoutOrderService, Order, OrderIsEmptyError
from src.shop.uow import BaseUnitOfWork


class CheckoutOrderServiceImpl(CheckoutOrderService):
    uow: BaseUnitOfWork

    def __init__(self, uow: BaseUnitOfWork):
        self.uow = uow

    async def checkout(self, order: Order, receiver_phone_number: str) -> Order:
        if not await self.uow.order_line_repo.get_by_order_id(order.id):
            raise OrderIsEmptyError("Order does not contain order lines")

        order.status = "waiting_for_approve"
        order.receiver_phone_number = receiver_phone_number
        return await self.uow.order_repo.persist(order)
