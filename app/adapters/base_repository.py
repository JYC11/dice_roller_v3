import abc
from typing import Any, TypeVar, Generic, Type

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.base import Base
from app.enums import enums


ModelType = TypeVar("ModelType", bound=Base)


class AbstractRepository(abc.ABC):
    def __init__(self):
        self.seen = set()

    def add(self) -> None:
        ...

    def get(self, ident: Any) -> Any:
        return self._get(ident)

    def list(self) -> Any:
        return self._list()

    def remove(self, obj: Any) -> Any:
        return self._remove(obj)

    def query_builder(self, kwargs):
        self._query_builder(**kwargs)
        return self

    def query_reset(self, kwargs):
        self._query_reset(**kwargs)
        return self

    def filter(self, *args, logical_operator: enums.LogicalOperatorEnum, **kwargs):
        self._filter(*args, logical_operator=logical_operator, **kwargs)
        return self

    def aggregate(self, func_name, criteria):
        self._aggregate(func_name, criteria)
        return self

    def group_by(self, *criteria):
        self._group_by(*criteria)
        return self

    def having(self, *criteria):
        self._having(*criteria)
        return self

    def order_by(self, criteria):
        self._order_by(criteria)
        return self

    def paginate(self, page, items_per_page):
        self._paginate(page, items_per_page)
        return self

    @abc.abstractmethod
    def _get(self, ident: Any) -> Any:
        ...

    @abc.abstractmethod
    def _list(self) -> Any:
        ...

    @abc.abstractmethod
    def _remove(self, obj: Any) -> Any:
        ...

    @abc.abstractmethod
    def _query_builder(self, kwargs):
        ...

    @abc.abstractmethod
    def _query_reset(self, kwargs):
        ...

    @abc.abstractmethod
    def _filter(self, *args, logical_operator, **kwargs):
        ...

    @abc.abstractmethod
    def _aggregate(self, func_name, criteria):
        ...

    @abc.abstractmethod
    def _group_by(self, criteria):
        ...

    @abc.abstractmethod
    def _having(self, criteria):
        ...

    @abc.abstractmethod
    def _order_by(self, criteria):
        ...

    @abc.abstractmethod
    def _paginate(self, page, items_per_page):
        ...


class SqlAlchemyRepository(Generic[ModelType], AbstractRepository):
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model
        self._base_query = select(self.model)

    # TODO: complete!
    def _get(self, ident: Any) -> Any:
        ...

    # TODO: complete!
    def _list(self) -> Any:
        ...

    # TODO: complete!
    def _remove(self, obj: Any) -> Any:
        ...

    # TODO: complete!
    def _query_builder(self, kwargs):
        ...

    # TODO: complete!
    def _query_reset(self, kwargs):
        ...

    # TODO: complete!
    def _filter(self, *args, logical_operator: enums.LogicalOperatorEnum, **kwargs):
        ...

    # TODO: complete!
    def _aggregate(self, func_name, criteria):
        ...

    # TODO: complete!
    def _group_by(self, criteria):
        ...

    # TODO: complete!
    def _having(self, criteria):
        ...

    # TODO: complete!
    def _order_by(self, criteria):
        ...

    # TODO: complete!
    def _paginate(self, page, items_per_page):
        ...
