import pytest
import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession

from src.shop.products.database import DatabaseProductRepository, Product
from src.shop.products.interfaces import Product as DomainProduct


@pytest.fixture
def product() -> DomainProduct:
    return DomainProduct(name="Samsung", price=1, discount=0)


@pytest.fixture
async def product_in_db(product: DomainProduct, db_session: AsyncSession) -> Product:
    query = sa.insert(Product).values([product.dict()]).returning(Product)
    product = (await db_session.execute(query)).fetchone()
    return Product(**product)


async def test_can_load_products(db_session: AsyncSession, product: DomainProduct):
    product1 = product
    product2 = DomainProduct(name="Macbook", category="laptops", price=123, discount=0)
    query = sa.insert(Product).values([product1.dict(), product2.dict()])

    await db_session.execute(query)
    select_query = sa.select(Product)
    products = (await db_session.execute(select_query)).scalars().all()
    domain_products = [DomainProduct.from_orm(product) for product in products]
    expected = [product1.dict(), product2.dict()]
    for product in domain_products:
        assert product.dict(exclude={"id"}) in expected


async def test_can_save_products(db_session: AsyncSession, product: DomainProduct):
    new_product = Product(**product.dict())
    await db_session.merge(new_product)
    [db_product] = (await db_session.execute(sa.select(Product))).scalars().all()
    assert db_product


async def test_db_user_repository_get(
    product_repo: DatabaseProductRepository, product_in_db: Product
):
    assert await product_repo.get(product_in_db.id) == DomainProduct.from_orm(
        product_in_db
    )


async def test_db_user_repository_not_exists(product_repo: DatabaseProductRepository):
    assert await product_repo.get(1) is None


async def test_db_user_repository_persist(
    product_repo: DatabaseProductRepository, product: DomainProduct
):
    product = await product_repo.persist(product)
    assert isinstance(product, DomainProduct)
    assert product.id
    assert await product_repo.get(product.id) == product
