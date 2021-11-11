from dependency_injector.containers import DeclarativeContainer
from dependency_injector.providers import Dependency, Singleton

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from src.shop.db.uow import SQLAlchemyUnitOfWork


class SqlAlchemyContainer(DeclarativeContainer):
    debug: Dependency[bool] = Dependency()
    url: Dependency[str] = Dependency()
    engine = Singleton(
        create_async_engine,
        url,
        echo=debug,
        future=True,
    )
    session_factory = Singleton(
        sessionmaker,
        engine,
        class_=AsyncSession,
        future=True,
    )
    uow = Singleton(
        SQLAlchemyUnitOfWork,
        session_factory=session_factory,
    )
