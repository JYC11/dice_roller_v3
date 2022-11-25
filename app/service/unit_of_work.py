import abc
from typing import Any

from sqlalchemy import text

from sqlalchemy.orm import Session

from app.adapters.base_repository import AbstractRepository, SqlAlchemyRepository
from app.common.db import SessionLocal


class AbstractUnitOfWork(abc.ABC):
    dnd_characters: AbstractRepository
    dnd_attacks: AbstractRepository
    dnd_damages: AbstractRepository

    def __enter__(self) -> "AbstractUnitOfWork":
        return (self,)

    def __exit__(self):
        self.rollback()

    def commit(self):
        self._commit()

    @abc.abstractmethod
    def _commit(self):
        ...

    def refresh(self, item: Any):
        self._refresh(item)

    @abc.abstractmethod
    def _refresh(self, item: Any):
        ...

    @abc.abstractmethod
    def rollback(self):
        pass

    @abc.abstractmethod
    def execute_raw_query(self, query: str) -> list[dict]:
        pass

    @abc.abstractmethod
    def collect_new_events(self):
        pass


DEFAULT_SESSION_FACTORY = SessionLocal


class SqlAlchemyUnitOfWork(AbstractUnitOfWork):
    def __init__(self, session_factory=DEFAULT_SESSION_FACTORY):
        self.session_factory = session_factory

    def __enter__(self):
        self.session: Session = self.session_factory()
        self.dnd_characters = SqlAlchemyRepository(self.session)
        self.dnd_attacks = SqlAlchemyRepository(self.session)
        self.dnd_damages = SqlAlchemyRepository(self.session)
        return super().__enter__()

    def __exit__(self, *args):
        super().__exit__(*args)
        self.session.close()

    def _commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

    def collect_new_events(self):
        for dnd_character in self.dnd_characters.seen:
            while dnd_character.events:
                yield dnd_character.events.pop(0)

    def execute_raw_query(self, query: str) -> list[dict]:
        rows = self.session.execute(text(query))  # type: ignore
        results: list[dict] = [dict(x) for x in rows.mappings().all()]
        return results
