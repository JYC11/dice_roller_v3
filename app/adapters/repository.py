import abc
from typing import Any, Sequence, TypeVar, Generic, Type

from sqlalchemy.orm import Session

from app.domain.base import Base


ModelType = TypeVar("ModelType", bound=Base)


class AbstractRepository(abc.ABC):
    @abc.abstractmethod
    def add(self, item: Any) -> None:
        ...

    @abc.abstractmethod
    def get(self, ident: Any) -> Any:
        ...

    @abc.abstractmethod
    def remove(self, ident: Any) -> Any:
        ...

    @abc.abstractmethod
    def list(
        self,
        ordering: dict[str | None] | None = None,
        **filters,
    ) -> Sequence[Any]:
        ...


class SqlAlchemyRepository(Generic[ModelType], AbstractRepository):
    def __init__(self, session: Session, model: Type[ModelType]):
        self.session = session
        self.model = model
        self._base_query = self.session.query(self.model)

    def add(self, item: ModelType) -> None:
        self.session.add(item)

    def get(self, ident: Any) -> ModelType | None:
        return self._base_query.filter(self.model.id == ident).first()

    def remove(self, ident: Any) -> None:
        db_obj = self.session.get(self.model, ident)
        self.session.delete(db_obj)
        return

    def commit(self):
        self.session.commit()

    def list(
        self,
        ordering: dict[str | None] | None = None,
        **filters,
    ) -> Sequence[ModelType]:
        return self._list(ordering=ordering, **filters)

    def _list(
        self,
        ordering: dict[str | None] | None = None,
        **filters,
    ):
        self._filter(**filters)
        self._base_query.order_by(*self._get_ordering_fields(ordering))
        return self._base_query.all()

    def _get_ordering_fields(self, ordering: dict[str | None]):
        return

    def _filter(self, **filter):
        return
