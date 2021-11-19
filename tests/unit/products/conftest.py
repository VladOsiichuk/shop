import pytest

from src.shop.products.interfaces import Product
from src.shop.products.memory import MemoryProductRepository


@pytest.fixture
async def product_in_db(product_repo: MemoryProductRepository) -> Product:
    product = Product(name="Iphone", category="phones", price=123, discount=0)
    return await product_repo.persist(product)
