from typing import List, Optional

from src.shop.products.interfaces import Product, ProductRepository


class MemoryProductRepository(ProductRepository):
    _db: dict[int, Product]
    _id_counter: int

    def __init__(self):
        self._db = {}
        self._id_counter = 1

    async def get(self, product_id: int) -> Optional[Product]:
        return self._db.get(product_id)

    async def get_by_name(self, name: str) -> Optional[Product]:
        for product in self._db.values():
            if product.name == name:
                return product

    async def get_by_category(self, category: str) -> List[Product]:
        result = []
        for product in self._db.values():
            if product.category == category:
                result.append(product)
        return result

    async def persist(self, product: Product) -> Product:
        product.id = self._id_counter
        self._db[self._id_counter] = product
        self._id_counter += 1
        return product

    async def list(self) -> List[Product]:
        return list(self._db.values())
