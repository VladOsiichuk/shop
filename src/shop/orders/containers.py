from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton

from src.shop.orders.interfaces import (
    CheckoutOrderService,
    CreateNewOrderUseCase,
    CheckoutOrderUseCase,
    AddOrderLineUseCase,
)
from src.shop.orders.services import CheckoutOrderServiceImpl
from src.shop.orders.use_cases import (
    CreateNewOrderUseCaseImpl,
    CheckoutOrderUseCaseImpl,
    AddOrderLineUseCaseImpl,
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
