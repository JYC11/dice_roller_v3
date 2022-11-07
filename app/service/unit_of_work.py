import abc
from typing import Any

from app.adapters.base_repository import AbstractRepository


class AbstractUnitOfWork(abc.ABC):
    dnd_character: AbstractRepository
    dnd_attack: AbstractRepository
    dnd_damage: AbstractRepository

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

    def collect_new_events(self):
        pass
