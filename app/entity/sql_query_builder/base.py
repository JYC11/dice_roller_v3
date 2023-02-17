from typing import List, Optional
from uuid import UUID

from app.enums import FilterOperatorEnum, LogicalOperatorEnum, QueryBuilderTypeEnum
from app.schemas import QueryBuilderFilterSchema

from .exceptions import InvalidConditionGiven

# THIS ONLY BUILDS QUERIES, NOT VALIDATE THEM. USE AT YOUR OWN RISK.


class QueryBuilder:
    def __init__(self, base_query: str):
        self.original_query = base_query
        self.base_query = base_query
        self.filter_list: list[QueryBuilderFilterSchema] = []
        self.ordering: Optional[str] = None
        self.array: Optional[List] = None
        self.array_column: Optional[str] = None
        self.page: Optional[int] = None
        self.items_per_page: Optional[int] = None

    def reset_query(self):
        self.base_query = self.original_query

    def get_query(self):
        self.reset_query()
        self._filter()
        self._order()
        self._paginate()
        return self.base_query

    def _apply_logical_operator(
        self, logical_operator, filter_index: int, filter_length: int
    ):
        if filter_index + 1 >= filter_length:
            return
        if logical_operator == LogicalOperatorEnum.AND.value:
            self.base_query += " AND\n"
        elif logical_operator == LogicalOperatorEnum.OR.value:
            self.base_query += " OR\n"

    def set_filters(self, filter_list: list[QueryBuilderFilterSchema]):
        self.filter_list = filter_list

    def _filter(self):
        if not self.filter_list:
            return self.base_query

        if not self.base_query.endswith("\n"):
            self.base_query += "\n"

        self.base_query += "WHERE \n"
        filter_len = len(self.filter_list)
        for idx in range(filter_len):
            _filter = self.filter_list[idx]
            column = _filter.column
            operator = _filter.operator
            value = _filter.value
            column_type = _filter.column_type
            logical_operator = _filter.logical_operator
            if operator == FilterOperatorEnum.EQ.value:
                if column_type == QueryBuilderTypeEnum.NUM.value:
                    self.base_query += f"{column} = {value}"
                elif column_type == QueryBuilderTypeEnum.BOOL.value:
                    self.base_query += f"{column} IS {str(value).upper()}"
                elif column_type == QueryBuilderTypeEnum.NULL.value:
                    self.base_query += f"{column} IS NULL"
                else:
                    self.base_query += f"{column} = '{value}'"
                self._apply_logical_operator(logical_operator, idx, filter_len)
            elif operator == FilterOperatorEnum.NOT_EQ.value:
                if column_type == QueryBuilderTypeEnum.NUM.value:
                    self.base_query += f"{column} != {value}"
                elif column_type == QueryBuilderTypeEnum.BOOL.value:
                    self.base_query += f"{column} IS NOT {str(value).upper()}"
                elif column_type == QueryBuilderTypeEnum.NULL.value:
                    self.base_query += f"{column} IS NOT NULL"
                else:
                    self.base_query += f"{column} != '{value}'"
                self._apply_logical_operator(logical_operator, idx, filter_len)
            elif operator == FilterOperatorEnum.GT.value:
                if column_type != QueryBuilderTypeEnum.NUM.value:
                    continue
                self.base_query += f"{column} > {value}"
                self._apply_logical_operator(logical_operator, idx, filter_len)
            elif operator == FilterOperatorEnum.GTE.value:
                if column_type != QueryBuilderTypeEnum.NUM.value:
                    continue
                self.base_query += f"{column} >= {value}"
                self._apply_logical_operator(logical_operator, idx, filter_len)
            elif operator == FilterOperatorEnum.LT.value:
                if column_type != QueryBuilderTypeEnum.NUM.value:
                    continue
                self.base_query += f"{column} < {value}"
                self._apply_logical_operator(logical_operator, idx, filter_len)
            elif operator == FilterOperatorEnum.LTE.value:
                if column_type != QueryBuilderTypeEnum.NUM.value:
                    continue
                self.base_query += f"{column} <= {value}"
                self._apply_logical_operator(logical_operator, idx, filter_len)
            elif operator == FilterOperatorEnum.IN.value:
                if type(value) != list:
                    continue
                in_array = ", ".join(value)
                self.base_query += f"{column} IN ({in_array})"
                self._apply_logical_operator(logical_operator, idx, filter_len)
            elif operator == FilterOperatorEnum.NOT_IN.value:
                if type(value) != list:
                    continue
                in_array = ", ".join(value)
                self.base_query += f"{column} NOT IN ({in_array})"
                self._apply_logical_operator(logical_operator, idx, filter_len)
            elif operator == FilterOperatorEnum.BTW.value:
                if type(value) != list or len(value) != 2:
                    continue
                low, high = value
                if column_type == QueryBuilderTypeEnum.NUM.value:
                    self.base_query += f"{column} BETWEEN {low} AND {high}"
                else:
                    self.base_query += f"{column} BETWEEN '{low}' AND '{high}'"
                self._apply_logical_operator(logical_operator, idx, filter_len)
            elif operator == FilterOperatorEnum.LIKE.value:
                if column_type != QueryBuilderTypeEnum.STR.value:
                    continue
                self.base_query += f"{column} LIKE '%{value}%'"
                self._apply_logical_operator(logical_operator, idx, filter_len)
            elif operator == FilterOperatorEnum.STARTS_WITH.value:
                if column_type != QueryBuilderTypeEnum.STR.value:
                    continue
                self.base_query += f"{column} LIKE '{value}%'"
                self._apply_logical_operator(logical_operator, idx, filter_len)
            elif operator == FilterOperatorEnum.ENDS_WITH.value:
                if column_type != QueryBuilderTypeEnum.STR.value:
                    continue
                self.base_query += f"{column} LIKE '%{value}'"
                self._apply_logical_operator(logical_operator, idx, filter_len)
            else:
                raise InvalidConditionGiven(f"No Such Operation Exists: {operator}")

    def set_orders(
        self,
        ordering: Optional[str] = None,
        array: Optional[List] = None,
        array_column: Optional[str] = None,
    ):
        self.ordering = ordering
        self.array = array
        self.array_column = array_column

    def _order(self):
        if not self.ordering:
            return self.base_query

        if not self.base_query.endswith("\n"):
            self.base_query += "\n"
        self.base_query += "ORDER BY "

        orderings = self.ordering.replace(" ", "").split(",")
        compiled_orderings = []
        for o in orderings:
            if o == "array_position":
                if not self.array or not self.array_column:
                    continue
                if type(self.array[0]) == UUID:
                    array_string = (
                        "ARRAY["
                        + ", ".join([f"'{str(x)}'" for x in self.array])
                        + "]::UUID[]"
                    )
                elif type(self.array[0]) == str:
                    array_string = (
                        "ARRAY[" + ", ".join([f"'{str(x)}'" for x in self.array]) + "]"
                    )
                else:
                    array_string = (
                        "ARRAY[" + ", ".join([str(x) for x in self.array]) + "]"
                    )
                array_ordering = f"ARRAY_POSITION({array_string}, {self.array_column})"
                compiled_orderings.append(array_ordering)
            elif o.startswith("-"):
                operator = "DESC"
                column = o.replace("-", "")
                compiled_orderings.append(f"{column} {operator}")
            else:
                operator = "ASC"
                column = o
                compiled_orderings.append(f"{column} {operator}")

        joined_orderings = ", ".join(compiled_orderings)
        self.base_query += f"{joined_orderings}\n"

    def set_pagination(self, page: int = 1, items_per_page: int = 20):
        self.page = page
        self.items_per_page = items_per_page

    def _paginate(self):
        if not self.base_query.endswith("\n"):
            self.base_query += "\n"

        if not self.items_per_page and not self.page:
            return

        if self.page != -1:
            offset_count = (self.page - 1) * self.items_per_page
            self.base_query += f"LIMIT {self.items_per_page} OFFSET {offset_count}\n"
        else:
            self.base_query += f"LIMIT {self.items_per_page}\n"
