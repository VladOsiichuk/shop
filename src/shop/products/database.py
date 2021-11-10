import sqlalchemy as sa
from shop.db import Base
from shop.products.interfaces import ProductRepository, Product as DomainProduct
from sqlalchemy.ext.asyncio import AsyncSession


class Product(Base):
    __tablename__ = "products"

    id = sa.Column(sa.BigInteger, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String)
    price = sa.Column(sa.Integer, default=1)
    discount = sa.Column(sa.Integer, default=0)
    category = sa.Column(sa.String, default="")


class DatabaseProductRepository(ProductRepository):
    def __init__(self, session: AsyncSession) -> None:
        self.db = session

    async def get(self, product_id: int) -> Optional[DomainProduct]:
        query = sa.select(Product).where(Product.id == product_id)
        product = (await self.db.execute(query)).scalars().one_or_none()
        if not product:
            return None
        return DomainProduct.from_orm(product)

    async def get_by_category(self, category: str) -> List[DomainProduct]:
        query = sa.select(Product).where(Product.category == category)
        products = (await self.db.execute(query)).scalars().all()

        return [DomainProduct.from_orm(db_obj) for db_obj in products]

    async def persist(self, product: DomainProduct) -> DomainProduct:
        query = sa.insert(Product).values(**product.dict()).returning(Product)
        db_object = (await self.db.execute(query)).fetchone()
        return DomainProduct.from_orm(db_object)

