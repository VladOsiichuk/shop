from pydantic import BaseModel
from abc import ABCMeta, abstractmethod


class Product(BaseModel):
    id: int
    name: str
    price: int
    discount: int

    @property
    def current_price(self):
        return round(self.price - (self.price / 100 * self.discount))

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
