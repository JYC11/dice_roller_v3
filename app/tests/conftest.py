import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from app.adapters.in_memory_orm import start_mappers, metadata
from app.tests.factories import user_input_factory


@pytest.fixture(scope="function")
def test_individual_raw_user_input_data() -> list[dict]:
    data = [user_input_factory() for _ in range(10)]
    return data


@pytest.fixture(scope="function")
def test_multiple_raw_user_input_data() -> list[tuple]:
    data = [(user_input_factory(), user_input_factory()) for _ in range(10)]
    return data


@pytest.fixture
def in_memory_db():
    engine = create_engine("sqlite:///:memory:")
    metadata.create_all(engine)
    return engine


@pytest.fixture
def session(in_memory_db):
    start_mappers()
    yield sessionmaker(bind=in_memory_db)()
    clear_mappers()
