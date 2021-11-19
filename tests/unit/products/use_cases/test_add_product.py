import pytest

from src.shop.products.interfaces import Product, ProductAlreadyExistsError
from src.shop.products.use_cases import AddProductUseCaseImpl
from src.shop.testing import DummyUnitOfWork


@pytest.fixture
def add_product_use_case(uow: DummyUnitOfWork) -> AddProductUseCaseImpl:
    return AddProductUseCaseImpl(uow=uow)


@pytest.mark.parametrize(
    "product_data",
    (
        {"name": "Iphone", "price": 123, "category": "Phones", "discount": 1},
        {"name": "Iphone", "price": 123, "discount": 1},
        {"name": "Iphone", "price": 123},
    ),
)
async def test_add_product_success(
    add_product_use_case: AddProductUseCaseImpl, product_data
):
    product = await add_product_use_case(**product_data)

    assert isinstance(product, Product)
    assert product.id
    assert product.name == product_data["name"]
    assert product.price == product_data["price"]
    assert product.category == product_data.get("category", None)
    assert product.discount == product_data.get("discount", 0)


async def test_add_product_product_exists(
    add_product_use_case: AddProductUseCaseImpl, product_in_db: Product
):
    with pytest.raises(ProductAlreadyExistsError):
        await add_product_use_case(
            name=product_in_db.name, price=product_in_db.price + 1
        )
