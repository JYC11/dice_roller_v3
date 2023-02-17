import abc
from typing import Any, TypeVar, Generic, Type

from sqlalchemy import select, and_, or_, func
from sqlalchemy.orm import Session
from sqlalchemy.orm.attributes import InstrumentedAttribute
from sqlalchemy.sql.selectable import Select

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

    def join(self, model, on, how):
        self._join(model, on, how)
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
    def _get(self) -> Any:
        ...

    @abc.abstractmethod
    def _list(self) -> Any:
        ...

    @abc.abstractmethod
    def _remove(self, obj: Any) -> Any:
        ...

    @abc.abstractmethod
    def _query_reset(self):
        ...

    @abc.abstractmethod
    def _filter(self, *args, logical_operator, **kwargs):
        ...

    @abc.abstractmethod
    def _join(self, model, on, how):
        ...

    @abc.abstractmethod
    def _aggregate(self, func_name, column_name):
        ...

    @abc.abstractmethod
    def _group_by(self, column_name):
        ...

    @abc.abstractmethod
    def _having(self, func_name, column_name):
        ...

    @abc.abstractmethod
    def _order_by(self, *args):
        ...

    @abc.abstractmethod
    def _paginate(self, page, items_per_page):
        ...


class SqlAlchemyRepository(Generic[ModelType], AbstractRepository):
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model
        self._base_query: Select = select(self.model)

    def _get(self) -> Any:
        return self.db.query(self._base_query).first()

    def _list(self) -> Any:
        return self.db.query(self._base_query).all()

    def _remove(self, obj: ModelType) -> Any:
        self.db.delete(obj)

    def _query_reset(self):
        self._base_query = select(self.model)

    # Maybe add relationship loading?

    # TODO: complete!
    def _filter(self, *args, logical_operator: enums.LogicalOperatorEnum, **kwargs):

        # What about filtering for columns from other models after joins?

        conditions = []
        for key, val in kwargs.items():
            match key.split("__"):
                case [column_name, operator]:
                    try:
                        column_name = getattr(self.model, column_name)
                    except AttributeError:
                        raise Exception  # TODO: write custom exception
                    else:
                        if operator == enums.FilterOperatorEnum.EQ.value:
                            conditions.append((column_name == val))
                        elif operator == enums.FilterOperatorEnum.NOT_EQ.value:
                            conditions.append((column_name != val))
                        elif operator == enums.FilterOperatorEnum.GT.value:
                            conditions.append((column_name > val))
                        elif operator == enums.FilterOperatorEnum.GTE.value:
                            conditions.append((column_name >= val))
                        elif operator == enums.FilterOperatorEnum.LT.value:
                            conditions.append((column_name < val))
                        elif operator == enums.FilterOperatorEnum.LTE.value:
                            conditions.append((column_name <= val))
                        elif operator == enums.FilterOperatorEnum.IN.value:
                            conditions.append((column_name.in_(val)))
                        elif operator == enums.FilterOperatorEnum.NOT_IN.value:
                            conditions.append((column_name.not_in(val)))
                        elif operator == enums.FilterOperatorEnum.BTW.value:
                            conditions.append((column_name.between(val)))
                        elif operator == enums.FilterOperatorEnum.LIKE.value:
                            conditions.append((column_name.ilike(f"%{val}%")))
                        elif operator == enums.FilterOperatorEnum.STARTS_WITH.value:
                            conditions.append((column_name.ilike(f"{val}%")))
                        elif operator == enums.FilterOperatorEnum.ENDS_WITH.value:
                            conditions.append((column_name.ilike(f"%{val}")))
                case _:
                    raise Exception  # TODO: write custom exception

        if logical_operator == enums.LogicalOperatorEnum.AND.value:
            self._base_query = self._base_query.where(and_(*conditions))
        else:
            self._base_query = self._base_query.where(or_(*conditions))

    # TODO: complete!
    def _join(self, model, on, how):
        ...

    def _aggregate(self, func_name, column_name):
        _function = getattr(func, func_name)
        column = self._get_column(column_name)
        self._base_query = select(column, _function(column))

    def _group_by(self, column_name):
        column = self._get_column(column_name)
        self._base_query = self._base_query.group_by(column)

    # TODO: complete!
    def _having(self, func_name, column_name):
        ...

    def _order_by(self, *args: str):
        for arg in args:
            column_name = arg
            is_ascending = True
            if arg.startswith("-"):
                is_ascending = False
                column_name = arg[1:]
            try:
                column = getattr(self.model, column_name)
                self._base_query = (
                    self._base_query.order_by(column.asc())
                    if is_ascending
                    else self._base_query.order_by(column.desc())
                )
            except:
                raise Exception

    def _paginate(self, page, items_per_page):
        if page != -1:
            self._base_query = self._base_query.offset(
                (page - 1) * items_per_page
            ).limit(items_per_page)
        else:
            self._base_query = self._base_query.limit(items_per_page)

    def _get_column(self, column_name):
        if column_name:
            try:
                column = getattr(self.model, column_name)
            except AttributeError:
                raise Exception
            else:
                return column
        else:
            return self
