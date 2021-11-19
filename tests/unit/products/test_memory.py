from src.shop.products.interfaces import Product
from src.shop.products.memory import MemoryProductRepository


async def test_persist(product_repo: MemoryProductRepository):
    product = await product_repo.persist(
        Product(name="Iphone", category="phones", price=123, discount=0)
    )
    assert isinstance(product, Product)
    assert product.id

    another_product = await product_repo.persist(
        Product(name="Iphone", category="phones", price=123, discount=0)
    )
    assert isinstance(another_product, Product)
    assert another_product.id
    assert another_product != product


async def test_get(product_repo: MemoryProductRepository, product_in_db: Product):
    product = await product_repo.get(product_in_db.id)
    assert product == product_in_db


async def test_get_product_not_exists(product_repo: MemoryProductRepository):
    assert await product_repo.get(1) is None


async def test_get_by_name(
    product_repo: MemoryProductRepository, product_in_db: Product
):
    assert await product_repo.get_by_name(product_in_db.name) == product_in_db


async def test_get_by_name_product_not_exists(product_repo: MemoryProductRepository):
    assert await product_repo.get_by_name("test") is None


async def test_list(product_repo: MemoryProductRepository):
    product1 = await product_repo.persist(Product(name="1", price=123, discount=0))
    product2 = await product_repo.persist(Product(name="2", price=123, discount=0))
    products = await product_repo.list()
    assert len(products) == 2
    assert product1 in products and product2 in products
