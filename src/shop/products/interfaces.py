from abc import ABCMeta, abstractmethod
from typing import List, Optional, Protocol

from pydantic import BaseModel

from src.shop.interfaces import DomainError


class Product(BaseModel):
    id: Optional[int]
    name: str
    category: Optional[str]
    price: int
    discount: int

    @property
    def discount_price(self):
        return round(self.price - (self.price / 100 * self.discount))

    def __eq__(self, other):
        return self.id == other.id

    def dict(self, *args, **kwargs):
        if not self.id:
            exclude = kwargs.get("exclude") or set()
            exclude.add("id")
            kwargs["exclude"] = exclude
        return super().dict(*args, **kwargs)

    class Config:
        orm_mode = True
        validate_assignment = True


class ProductRepository(metaclass=ABCMeta):
    @abstractmethod
    async def get(self, product_id: int) -> Optional[Product]:
        """
        :param product_id: ID of product
        :return: Product instance
        """
        pass

    @abstractmethod
    async def get_by_category(self, category: str) -> List[Product]:
        """
        :param category: category name
        :return: list of products by provided category
        """
        pass

    @abstractmethod
    async def persist(self, product: Product) -> Product:
        """
        :param product: Product instance
        :return: Product with id
        """
        pass

    @abstractmethod
    async def get_by_name(self, name: str) -> Optional[Product]:
        """
        Args:
            name: product_name

        Returns:
            Product if exists
        """
        pass

    @abstractmethod
    async def list(self) -> List[Product]:
        """
        Returns: List of all products

        """
        pass


class ProductAlreadyExistsError(DomainError):
    pass


class ProductDoesNotExists(DomainError):
    pass


class AddProductUseCase(Protocol):
    async def __call__(
        self,
        name: str,
        price: int,
        category: Optional[str] = None,
        discount: Optional[int] = 0,
    ) -> Product:
        """
        As a shop user, I want to add a new product
        Args:
            name: Product name
            price: price
            category: Category name
            discount: Optional discount for current product
        Raises:
            ProductAlreadyExistsError: If product with specified name already exists
        Returns:
            Product instance
        """


class ViewAllProductsUseCase(Protocol):
    async def __call__(self) -> List[Product]:
        """
        As a shop customer, I want to view all existing products
        Returns:
            list of products
        """


class ViewCategoryProducts(Protocol):
    async def __call__(self, category: str) -> List[Product]:
        """
        As a shop customer, I want to view category related products
        Returns:
            list of products from specified category
        """
