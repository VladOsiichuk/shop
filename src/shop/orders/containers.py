from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton

from src.shop.orders.interfaces import (
    AddOrderLineUseCase,
    CheckoutOrderService,
    CheckoutOrderUseCase,
    CreateNewOrderUseCase,
)
from src.shop.orders.services import CheckoutOrderServiceImpl
from src.shop.orders.use_cases import (
    AddOrderLineUseCaseImpl,
    CheckoutOrderUseCaseImpl,
    CreateNewOrderUseCaseImpl,
)
from src.shop.uow import BaseUnitOfWork


class OrderCasesCasesContainer(DeclarativeContainer):
    uow: Dependency[BaseUnitOfWork] = Dependency()

    checkout_service: Singleton[CheckoutOrderService] = Singleton(
        CheckoutOrderServiceImpl, uow=uow
    )
    create_order: Singleton[CreateNewOrderUseCase] = Singleton(
        CreateNewOrderUseCaseImpl, uow=uow
    )
    checkout_order: Singleton[CheckoutOrderUseCase] = Singleton(
        CheckoutOrderUseCaseImpl, uow=uow
    )
    add_order_line: Singleton[AddOrderLineUseCase] = Singleton(
        AddOrderLineUseCaseImpl, uow=uow
    )
