import sys
from typing import Generator

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session, clear_mappers
from sqlalchemy.orm import Session, close_all_sessions

from app.common.db import engine
from app.adapters.in_memory_orm import start_mappers, metadata
from app.tests.factories.input import user_input_factory


@pytest.fixture(scope="function")
def test_individual_raw_user_input_data() -> list[dict]:
    data = [user_input_factory() for _ in range(10)]
    return data


@pytest.fixture(scope="function")
def test_multiple_raw_user_input_data() -> list[tuple]:
    data = [(user_input_factory(), user_input_factory()) for _ in range(10)]
    return data


@pytest.fixture(scope="session")
def db_engine() -> Generator:
    metadata.create_all(engine)
    yield engine
    close_all_sessions()
    clear_mappers()


@pytest.fixture(scope="function")
def session_factory(db_engine):
    connection = db_engine.connect()
    transaction = connection.begin()

    SessionFactory = scoped_session(sessionmaker(autoflush=False, bind=connection))
    from app.tests import factories  # noqa

    factory_module = sys.modules.get("app.tests.factories")
    for key in factory_module.__dict__.keys():
        if "Factory" in key and "Mixin" not in key and "Base" not in key:
            exec(f"factory_module.{key}._meta.sqlalchemy_session = SessionFactory")

    yield SessionFactory

    transaction.rollback()
    SessionFactory.expunge_all()
    connection.close()


@pytest.fixture(scope="function")
def db(session_factory) -> Generator:
    session_inst = session_factory()
    try:
        yield session_inst
    except Exception as e:
        session_inst.rollback()
        raise e
    finally:
        session_inst.close()
