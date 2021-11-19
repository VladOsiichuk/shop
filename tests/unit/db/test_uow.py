from sqlite3 import OperationalError

import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.engine import Engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker

from src.shop.db.uow import SessionFactory, SQLAlchemyUnitOfWork


@pytest.fixture
async def engine() -> Engine:
    engine = create_async_engine("sqlite+aiosqlite:///:memory:", future=True)
    async with engine.connect():
        yield engine


@pytest.fixture
def session_factory(engine: Engine) -> SessionFactory:
    return sessionmaker(engine, future=True, class_=AsyncSession)


@pytest.fixture
def uow(session_factory: SessionFactory) -> SQLAlchemyUnitOfWork:
    return SQLAlchemyUnitOfWork(session_factory)


async def test_non_reentrant(uow: SQLAlchemyUnitOfWork) -> None:
    with pytest.raises(RuntimeError, match=r"UoW is already working"):
        async with uow:
            async with uow:
                pass


async def test_reuse_uow(uow: SQLAlchemyUnitOfWork) -> None:
    async with uow:
        session_first = uow._session

    assert not uow._session

    async with uow:
        session_second = uow._session

    assert not uow._session

    assert session_first is not session_second


async def test_commit(uow: SQLAlchemyUnitOfWork) -> None:
    async with uow:
        s = uow._session

        assert s is not None

        await s.execute(text("create table test (id int PRIMARY KEY)"))
        await s.execute(text("insert into test (id) values (123)"))

        await uow.commit()

    assert uow._session is None
    assert (await s.execute(text("select * from test"))).all() == [(123,)]


async def test_rollback(uow: SQLAlchemyUnitOfWork) -> None:
    async with uow:
        s = uow._session

        assert s is not None

        await s.execute(text("create table test_table (id int PRIMARY KEY)"))
        await s.execute(text("insert into test_table (id) values (56)"))

        await uow.rollback()

    assert uow._session is None
    assert (
        await s.execute(text("SELECT * FROM sqlite_master where type='test'"))
    ).all() == []


async def test_implicit_rollback(uow: SQLAlchemyUnitOfWork) -> None:
    async with uow:
        s = uow._session

        assert s is not None

        await s.execute(text("create table test (id int PRIMARY KEY)"))
        await s.execute(text("insert into test (id) values (123)"))

    assert uow._session is None
    assert (await s.execute(text("select * from test"))).all() == []
