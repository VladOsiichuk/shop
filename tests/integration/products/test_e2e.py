import pytest
from httpx import AsyncClient
from starlette import status

from src.shop.products.database import DatabaseProductRepository
from src.shop.products.interfaces import Product
from tests.integration.products.constants import ADD_PRODUCT_URL, VIEW_ALL_PRODUCTS_URL

pytestmark = pytest.mark.usefixtures("db_session")


async def test_add_product_success(
    client: AsyncClient, product_repo: DatabaseProductRepository
):
    expected_data = {"name": "Samsung", "category": "Laptops", "price": 233}
    response = await client.post(ADD_PRODUCT_URL, json=expected_data)
    assert response.status_code == status.HTTP_201_CREATED

    expected_fields = {"id", "category", "price", "discount", "name"}
    actual_data = response.json()
    assert not set(actual_data.keys()) - expected_fields

    for field, value in expected_data.items():
        assert actual_data[field] == value

    assert await product_repo.get(actual_data["id"])


@pytest.mark.parametrize(
    "data",
    (
        {"name": "", "price": 123},
        {"name": "test", "price": None},
        {"name": None, "price": 345},
    ),
)
async def test_add_product_invalid_data(client: AsyncClient, data: dict):
    response = await client.post(ADD_PRODUCT_URL, json=data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


async def test_view_all_products(
    client: AsyncClient, product_repo: DatabaseProductRepository
):
    product1 = await product_repo.persist(Product(name="test1", price=222, discount=1))
    product2 = await product_repo.persist(Product(name="test2", price=111, discount=0))
    product_ids = [product1.id, product2.id]
    resp = await client.get(VIEW_ALL_PRODUCTS_URL)
    assert resp.status_code == status.HTTP_200_OK
    data = resp.json()
    assert isinstance(data.get("results"), list)
    assert len(data["results"]) == 2
    for product in data["results"]:
        assert product["id"] in product_ids
