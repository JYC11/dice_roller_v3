import abc
from typing import Any, Sequence, TypeVar, Generic, Type

from sqlalchemy import and_, or_, func
from sqlalchemy.orm import Session, Query
from sqlalchemy.orm.attributes import InstrumentedAttribute

from app.domain.base import Base
from .exception import InvalidColumn, InvalidConditionGiven, AttributeNotExist


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

    @abc.abstractmethod
    def paginated_list(
        self,
        page: int,
        items_per_page: int,
        search_query: dict[str, Any] | None,
        ordering: str | None,
        **kwargs,
    ) -> tuple[Sequence[Any], int]:
        ...


class SqlAlchemyRepository(Generic[ModelType], AbstractRepository):
    def __init__(self, db: Session, model: Type[ModelType]):
        self.db = db
        self.model = model
        self._base_query = self.db.query(self.model)

    def _search_query(self, query: Query, search_query: dict[str, Any] | None):
        if search_query is None:
            return query

        for search_type, keyword in search_query.items():
            attribute = getattr(self.model, search_type)
            query.filter(attribute.ilike(f"%{keyword}"))
        return query

    def _order_query(self, query: Query, ordering: str | None = None):
        if not ordering:
            return query
        return query.order_by(*self._get_ordering_fields(ordering))

    def _get_ordering_fields(self, ordering_query_str: str | None) -> list:
        """
        Return ordering expression list applied ASC or DESC for order_by of sqlalchemy
        """
        # Preprocessing query string
        ordering_list = ordering_query_str.split(",") if ordering_query_str else []

        ordering_fields = []
        try:
            default_ordering_by_create_dt = getattr(self.model, "create_dt")
        except AttributeError:
            default_ordering_by_create_dt = getattr(self.model, "id")
        for col_name in ordering_list:
            if col_name:
                """
                regular ordering
                1. first check desc or asc by checking '-'
                2. check if ordering on nested json
                    col_name_json_check > implements nested json field ordering
                """
                desc = False
                if col_name.startswith("-"):
                    desc = True
                    col_name = col_name[1:]
                col_name_json_check = col_name.split("__")

                model_column = getattr(self.model, col_name_json_check[0])
                if len(col_name_json_check) == 2:
                    model_column = model_column[col_name_json_check[1]]
                if desc:
                    ordering_fields.append(model_column.desc())
                else:
                    ordering_fields.append(model_column.asc())

        # Default: create_dt.desc()
        if not ordering_fields:
            ordering_fields.append(default_ordering_by_create_dt.desc())
        ordering_fields.append("id")
        return ordering_fields

    def _list(
        self,
        search_query: dict[str, Any] | None = None,
        ordering: str | None = None,
        **kwargs,
    ) -> Query:
        query = self._base_query.filter_by(**kwargs)
        query = self._search_query(query=query, search_query=search_query)
        query = query.order_by(*self._get_ordering_fields(ordering))
        return query

    def add(self, item: ModelType) -> None:
        # obj = self.model(**item.dict())
        self.db.add(item)

    def get(self, ident: Any) -> ModelType | None:
        return self._base_query.filter(self.model.id == ident).first()

    def paginated_list(
        self,
        page: int = 1,
        items_per_page: int = 20,
        search_query: dict[str, Any] = None,
        ordering: str | None = None,
        **kwargs,
    ) -> tuple[Sequence[ModelType], int]:
        query = self._list(search_query=search_query, ordering=ordering, **kwargs)
        total = query.count()
        if items_per_page < 0:
            items_per_page = total
        offset = (page - 1) * items_per_page
        query = self._order_query(query=query, ordering=ordering)
        query = query.offset(offset).limit(items_per_page)
        return query.all(), total

    def list(
        self,
        search_query: dict[str, Any] = None,
        ordering: str | None = None,
        **filters,
    ) -> Sequence[ModelType]:
        return self._list(search_query=search_query, ordering=ordering, **filters).all()

    def remove(self, ident: Any) -> None:
        db_obj = self.db.get(self.model, ident)
        self.db.delete(db_obj)
        return

    def commit(self):
        self.db.commit()
