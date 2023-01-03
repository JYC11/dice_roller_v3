import ast
from typing import Any

# from app.enums import FilterOperatorEnum, LogicalOperatorEnum, QueryBuilderTypeEnum
from app.schemas import QueryBuilderFilterSchema


def search_query_parser(search_query: dict[str, Any] = None):
    filters: list[QueryBuilderFilterSchema] = []
    if search_query:
        for (k, v) in search_query.items():
            continue
    return filters
