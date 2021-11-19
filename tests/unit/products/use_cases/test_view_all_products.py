import pytest

from src.shop.products.interfaces import Product
from src.shop.products.memory import MemoryProductRepository
from src.shop.products.use_cases import ViewAllProductsUseCaseImpl
from src.shop.testing import DummyUnitOfWork


@pytest.fixture
def view_all_products_use_case(uow: DummyUnitOfWork) -> ViewAllProductsUseCaseImpl:
    return ViewAllProductsUseCaseImpl(uow=uow)


async def test_view_all_products(
    view_all_products_use_case: ViewAllProductsUseCaseImpl,
    product_repo: MemoryProductRepository,
):
    product1 = await product_repo.persist(Product(name="1", price=222, discount=1))
    product2 = await product_repo.persist(Product(name="2", price=333, discount=0))
    product3 = await product_repo.persist(Product(name="3", price=444, discount=2))
    expected = [product3, product2, product1]
    results = await view_all_products_use_case()
    assert len(results) == 3

    for product in results:
        assert product in expected
