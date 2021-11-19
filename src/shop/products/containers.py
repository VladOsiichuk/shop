from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton

from src.shop.products.interfaces import (
    AddProductUseCase,
    ViewAllProductsUseCase,
    ViewCategoryProducts,
)
from src.shop.products.use_cases import (
    AddProductUseCaseImpl,
    ViewAllProductsUseCaseImpl,
    ViewCategoryProductsImpl,
)
from src.shop.uow import BaseUnitOfWork


class ProductCasesContainer(DeclarativeContainer):
    uow: Dependency[BaseUnitOfWork] = Dependency()

    add_product: Singleton[AddProductUseCase] = Singleton(
        AddProductUseCaseImpl,
        uow=uow,
    )
    view_all_products: Singleton[ViewAllProductsUseCase] = Singleton(
        ViewAllProductsUseCaseImpl, uow=uow
    )
    view_category_products: Singleton[ViewCategoryProducts] = Singleton(
        ViewCategoryProductsImpl, uow=uow
    )
