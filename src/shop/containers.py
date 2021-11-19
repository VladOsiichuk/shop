import sys
from importlib import import_module
from pkgutil import walk_packages
from types import ModuleType
from typing import Iterator, Set

from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Configuration
from dependency_injector.providers import Container as ContainerProvider

from src.shop.db.container import SqlAlchemyContainer
from src.shop.orders.containers import OrderCasesCasesContainer
from src.shop.products.containers import ProductCasesContainer
from src.shop.settings import Settings


class Container(DeclarativeContainer):
    config = Configuration()

    db = ContainerProvider(
        SqlAlchemyContainer,
        url=config.db.url,
        debug=config.db.debug,
    )
    product_use_cases = ContainerProvider(ProductCasesContainer, uow=db.uow)
    order_use_cases = ContainerProvider(OrderCasesCasesContainer, uow=db.uow)


def find_modules(package: ModuleType, excluded: Set[str]) -> Iterator[ModuleType]:
    """Helper to run imports

    Returns:
        Iterator with modules

    """
    yield package

    for module_info in walk_packages(
        package.__path__,  # type: ignore[attr-defined]
        package.__name__ + ".",
    ):
        if module_info.name not in excluded:
            yield import_module(module_info.name)


def bootstrap() -> Container:
    container = Container()

    container.config.from_pydantic(Settings())

    excluded = set(container.config.do_not_wire())
    modules = list(find_modules(sys.modules["src"], excluded))

    container.wire(modules=modules)
    container.init_resources()

    return container
