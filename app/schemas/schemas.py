from decimal import Decimal
from enum import Enum
from uuid import UUID

from pydantic import BaseModel

from app.enums import FilterOperatorEnum, QueryBuilderTypeEnum, LogicalOperatorEnum


class QueryBuilderFilterSchema(BaseModel):
    column: str
    operator: FilterOperatorEnum
    value: str | float | int | bool | Decimal | Enum | UUID | list
    column_type: QueryBuilderTypeEnum
    logical_operator: LogicalOperatorEnum
