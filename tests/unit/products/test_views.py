from typing import Callable

import pytest
from starlette.exceptions import HTTPException

from src.shop.products.interfaces import Product, ProductAlreadyExistsError
from src.shop.products.schemas import AddProductRequestSchema
from src.shop.products.views import add_product


@pytest.fixture
def add_product_request_schema():
    return AddProductRequestSchema(name="test", category="laptops", price=1, discount=0)


@pytest.fixture
async def add_product_success_use_case(
    add_product_request_schema: AddProductRequestSchema,
):
    async def _inner(*args, **kwargs):
        return Product(
            name=add_product_request_schema.name,
            category=add_product_request_schema.category,
            price=add_product_request_schema.price,
            discount=add_product_request_schema.discount,
            id=1,
        )

    return _inner


@pytest.fixture
async def add_product_raises_error_use_case():
    async def _inner(*args, **kwargs):
        raise ProductAlreadyExistsError()

    return _inner


async def test_add_product_view_success(
    add_product_request_schema: AddProductRequestSchema,
    add_product_success_use_case: Callable,
):
    res = await add_product(
        data=add_product_request_schema,
        add_product_use_case=add_product_success_use_case,
    )
    assert isinstance(res, Product)


async def test_add_product_fail(
    add_product_request_schema: AddProductRequestSchema,
    add_product_raises_error_use_case: Callable,
):
    with pytest.raises(HTTPException, match=str(ProductAlreadyExistsError())):
        await add_product(
            data=add_product_request_schema,
            add_product_use_case=add_product_raises_error_use_case,
        )
