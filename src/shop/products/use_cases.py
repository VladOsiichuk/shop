from typing import Optional, List
from src.shop.uow import BaseUnitOfWork
from src.shop.products.interfaces import (
    AddProductUseCase,
    ProductAlreadyExistsError,
    ViewAllProductsUseCase,
    ViewCategoryProducts,
)
from src.shop.products.interfaces import Product


class AddProductUseCaseImpl(AddProductUseCase):
    uow: BaseUnitOfWork

    def __init__(self, uow: BaseUnitOfWork):
        self.uow = uow

    async def __call__(
        self,
        name: str,
        price: int,
        category: Optional[str] = None,
        discount: Optional[int] = 0,
    ) -> Product:
        product = Product(name=name, price=price, category=category, discount=discount)

        async with self.uow as uow:
            if await uow.product_repo.get_by_name(name):
                raise ProductAlreadyExistsError(
                    "Product with specified name already exists"
                )

            product = await uow.product_repo.persist(product)
            await uow.commit()
            return product


class ViewAllProductsUseCaseImpl(ViewAllProductsUseCase):
    uow: BaseUnitOfWork

    def __init__(self, uow: BaseUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self):
        async with self.uow as uow:
            return await uow.product_repo.list()


class ViewCategoryProductsImpl(ViewCategoryProducts):
    uow: BaseUnitOfWork

    def __init__(self, uow: BaseUnitOfWork) -> None:
        self.uow = uow

    async def __call__(self, category: str) -> List[Product]:
        async with self.uow as uow:
            return await uow.product_repo.get_by_category(category=category)
