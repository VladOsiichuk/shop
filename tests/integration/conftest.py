import asyncio
from typing import Any, Iterator

import asyncpg
import pytest
from dependency_injector.providers import OverridingContext
from fastapi import FastAPI
from fastapi.testclient import TestClient
from httpx import AsyncClient
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession

from src.shop.containers import Container, bootstrap
from src.shop.db import Base, metadata
from src.shop.products.database import DatabaseProductRepository
from src.shop.settings import DatabaseSettings
from src.shop.web.app import create_app


@pytest.fixture(scope="session")
def db_url(worker_id: int) -> str:
    db_url = DatabaseSettings().url
    url, db_url = db_url.rsplit("/", maxsplit=1)
    return f"{url}/test_{db_url}_{worker_id}"


@pytest.fixture(scope="session")
async def test_db(db_url: str) -> None:
    db_url = db_url.replace("postgresql+asyncpg://", "postgresql://")
    db_url, db_name = db_url.rsplit("/", maxsplit=1)
    conn = await asyncpg.connect(db_url)
    await conn.execute("COMMIT")
    await conn.execute(f"DROP DATABASE IF EXISTS {db_name}")
    await conn.execute(f"CREATE DATABASE {db_name}")
    yield
    await conn.close()


@pytest.fixture
async def db_session(test_db, container: Container):
    override_engine: OverridingContext[Any]
    override_session: OverridingContext[Any]
    engine: AsyncEngine = container.db.engine()
    conn = await engine.connect()
    await conn.run_sync(Base.metadata.create_all)
    trans = conn.get_transaction()

    async with AsyncSession(bind=conn, future=True) as session:
        await session.begin_nested()

        @event.listens_for(session.sync_session, "after_transaction_end")
        def restart_savepoint(session, transaction):
            if transaction.nested and not transaction._parent.nested:
                session.begin_nested()

        override_engine = container.db.engine.override(engine)
        override_session = container.db.session_factory.override(lambda: session)

        with override_engine, override_session:
            yield session

    await trans.rollback()
    await conn.close()
    await engine.dispose()


@pytest.fixture(scope="session")
def _container(db_url: str) -> Iterator[Container]:
    container = bootstrap()

    with container.config.db.url.override(db_url):
        yield container


@pytest.fixture
def container(_container: Container) -> Iterator[Container]:
    with _container.reset_singletons():
        yield _container
        _container.shutdown_resources()


@pytest.fixture
def fastapi_app(container: Container) -> FastAPI:
    return create_app(lambda: container)


@pytest.fixture
async def client(fastapi_app: FastAPI) -> TestClient:
    async with AsyncClient(app=fastapi_app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def product_repo(db_session: AsyncSession) -> DatabaseProductRepository:
    return DatabaseProductRepository(db_session)
