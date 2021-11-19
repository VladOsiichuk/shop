import pytest

from src.shop.products.interfaces import Product


@pytest.mark.parametrize(
    "price,discount,expected", ((100, 0, 100), (100, 100, 0), (100, 50, 50))
)
async def test_product_discount(price: int, discount: int, expected: int):
    product = Product(name="Samsung", price=price, discount=discount)
    assert product.discount_price == expected
