from typing import Any, Callable

from sqlalchemy import create_engine
from app.adapters.in_memory_orm import metadata, start_mappers
from app.core import config as settings
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm.session import sessionmaker

engine = None
autocommit_engine = None
SessionLocal: None | Callable = None


def in_memory_db(url):
    engine = create_engine(url, connect_args={"check_same_thread": False}, future=True)
    metadata.create_all(engine)
    return engine


if settings.STAGE in ("testing", "ci-testing"):
    engine = in_memory_db("sqlite+pysqlite:///:memory:")
    conn = engine.connect()
    start_mappers()
    SessionLocal = scoped_session(
        sessionmaker(
            autocommit=False, autoflush=False, bind=engine, expire_on_commit=False
        )
    )
