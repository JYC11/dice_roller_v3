from uuid import uuid4

from app.entity.sql_query_builder import QueryBuilder
from app.enums import FilterOperatorEnum, LogicalOperatorEnum, QueryBuilderTypeEnum
from app.schemas import QueryBuilderFilterSchema


def test_query_builder_logical_operator(base_query):
    builder = QueryBuilder(base_query + "WHERE name = 'foobar'")
    filter_len = 3
    builder._apply_logical_operator("and", 2, filter_len)
    query1 = builder.base_query
    assert query1[-4:] != "AND\n"

    builder._apply_logical_operator("and", 0, filter_len)
    query2 = builder.base_query
    assert query2[-4:] == "AND\n"


def test_query_builder_filtering(base_query):
    char_id_strings = [f"'{str(uuid4())}'" for _ in range(2)]

    builder = QueryBuilder(base_query)
    filters = [
        QueryBuilderFilterSchema(
            column="name",
            operator=FilterOperatorEnum.EQ,
            value="foobar",
            column_type=QueryBuilderTypeEnum.STR,
            logical_operator=LogicalOperatorEnum.AND,
        ),
        QueryBuilderFilterSchema(
            column="level",
            operator=FilterOperatorEnum.GT,
            value=3,
            column_type=QueryBuilderTypeEnum.NUM,
            logical_operator=LogicalOperatorEnum.OR,
        ),
        QueryBuilderFilterSchema(
            column="proficiency",
            operator=FilterOperatorEnum.GTE,
            value=2,
            column_type=QueryBuilderTypeEnum.NUM,
            logical_operator=LogicalOperatorEnum.AND,
        ),
        QueryBuilderFilterSchema(
            column="strength",
            operator=FilterOperatorEnum.LT,
            value=15,
            column_type=QueryBuilderTypeEnum.NUM,
            logical_operator=LogicalOperatorEnum.OR,
        ),
        QueryBuilderFilterSchema(
            column="charisma",
            operator=FilterOperatorEnum.LTE,
            value=10,
            column_type=QueryBuilderTypeEnum.NUM,
            logical_operator=LogicalOperatorEnum.AND,
        ),
        QueryBuilderFilterSchema(
            column="dexterity",
            operator=FilterOperatorEnum.BTW,
            value=[10, 20],
            column_type=QueryBuilderTypeEnum.NUM,
            logical_operator=LogicalOperatorEnum.OR,
        ),
        QueryBuilderFilterSchema(
            column="create_dt",
            operator=FilterOperatorEnum.BTW,
            value=["2022-01-01", "2022-12-31"],
            column_type=QueryBuilderTypeEnum.DATE,
            logical_operator=LogicalOperatorEnum.AND,
        ),
        QueryBuilderFilterSchema(
            column="class_info",
            operator=FilterOperatorEnum.LIKE,
            value="Path",
            column_type=QueryBuilderTypeEnum.STR,
            logical_operator=LogicalOperatorEnum.OR,
        ),
        QueryBuilderFilterSchema(
            column="finesse",
            operator=FilterOperatorEnum.EQ,
            value=False,
            column_type=QueryBuilderTypeEnum.BOOL,
            logical_operator=LogicalOperatorEnum.AND,
        ),
        QueryBuilderFilterSchema(
            column="id",
            operator=FilterOperatorEnum.IN,
            value=char_id_strings,
            column_type=QueryBuilderTypeEnum.STR,
            logical_operator=LogicalOperatorEnum.OR,
        ),
        QueryBuilderFilterSchema(
            column="id",
            operator=FilterOperatorEnum.NOT_IN,
            value=char_id_strings,
            column_type=QueryBuilderTypeEnum.STR,
            logical_operator=LogicalOperatorEnum.AND,
        ),
        QueryBuilderFilterSchema(
            column="armour_class",
            operator=FilterOperatorEnum.IN,
            value=["10", "15", "20"],
            column_type=QueryBuilderTypeEnum.NUM,
            logical_operator=LogicalOperatorEnum.AND,
        ),
        QueryBuilderFilterSchema(
            column="class_info",
            operator=FilterOperatorEnum.EQ,
            value="null",
            column_type=QueryBuilderTypeEnum.NULL,
            logical_operator=LogicalOperatorEnum.OR,
        ),
        QueryBuilderFilterSchema(
            column="class_info",
            operator=FilterOperatorEnum.STARTS_WITH,
            value="Oath",
            column_type=QueryBuilderTypeEnum.STR,
            logical_operator=LogicalOperatorEnum.AND,
        ),
    ]
    expected_filters = [
        "name = 'foobar' AND",
        "level > 3 OR",
        "proficiency >= 2 AND",
        "strength < 15 OR",
        "charisma <= 10 AND",
        "dexterity BETWEEN 10 AND 20 OR",
        "create_dt BETWEEN '2022-01-01' AND '2022-12-31' AND",
        "class_info LIKE '%Path%' OR",
        "finesse IS FALSE AND",
        f"id IN ({', '.join(char_id_strings)}) OR",
        f"id NOT IN ({', '.join(char_id_strings)}) AND",
        "armour_class IN (10, 15, 20) AND",
        "class_info IS NULL OR",
        "class_info LIKE 'Oath%'",
    ]
    builder.set_filters(filters)
    filtered_query = builder.get_query()
    compiled_filters = [x for x in filtered_query.split("\n") if x][-14:]

    for expected, actual in zip(expected_filters, compiled_filters):
        assert expected == actual


def test_query_builder_ordering(base_query):
    builder = QueryBuilder(base_query)
    builder.set_orders(ordering="-create_dt,update_dt")
    ordered_query = builder.get_query()
    expected_ordering = "ORDER BY create_dt DESC, update_dt ASC"
    split_up = [x for x in ordered_query.split("\n") if len(x) > 0]
    assert split_up[-1].strip() == expected_ordering


def test_query_builder_array_position_ordering(base_query):
    rnd_product_ids = [uuid4() for _ in range(2)]
    rnd_product_id_strings = [f"'{str(x)}'" for x in rnd_product_ids]

    builder = QueryBuilder(base_query)
    builder.set_orders(
        ordering="array_position", array=rnd_product_ids, array_column="id"
    )
    ordered_query1 = builder.get_query()
    expected_ordering1 = f"ORDER BY ARRAY_POSITION(ARRAY[{', '.join(rnd_product_id_strings)}]::UUID[], id)"
    split_up1 = [x for x in ordered_query1.split("\n") if len(x) > 0]
    assert split_up1[-1].strip() == expected_ordering1

    builder.reset_query()

    rnd_names1 = ["foo", "bar", "baz"]
    rnd_names2 = ["'foo'", "'bar'", "'baz'"]
    builder.set_orders(ordering="array_position", array=rnd_names1, array_column="name")
    ordered_query2 = builder.get_query()
    expected_ordering2 = (
        f"ORDER BY ARRAY_POSITION(ARRAY[{', '.join(rnd_names2)}], name)"
    )
    split_up2 = [x for x in ordered_query2.split("\n") if len(x) > 0]
    assert split_up2[-1].strip() == expected_ordering2

    builder.reset_query()

    rnd_prices1 = [10, 20, 30]
    rnd_prices2 = ["10", "20", "30"]
    builder.set_orders(
        ordering="array_position", array=rnd_prices1, array_column="armour_class"
    )
    ordered_query3 = builder.get_query()
    expected_ordering3 = (
        f"ORDER BY ARRAY_POSITION(ARRAY[{', '.join(rnd_prices2)}], armour_class)"
    )
    split_up3 = [x for x in ordered_query3.split("\n") if len(x) > 0]
    assert split_up3[-1].strip() == expected_ordering3


def test_query_builder_paginating(base_query):
    builder = QueryBuilder(base_query)
    builder.set_pagination(page=1, items_per_page=20)
    paginated_query1 = builder.get_query()
    expected_pagination1 = "LIMIT 20 OFFSET 0"
    split_up = [x for x in paginated_query1.split("\n") if len(x) > 0]
    assert split_up[-1].strip() == expected_pagination1

    builder.reset_query()

    builder.set_pagination(page=2, items_per_page=20)
    paginated_query2 = builder.get_query()
    expected_pagination2 = "LIMIT 20 OFFSET 20"
    split_up = [x for x in paginated_query2.split("\n") if len(x) > 0]
    assert split_up[-1].strip() == expected_pagination2

    builder.reset_query()

    builder.set_pagination(page=-1, items_per_page=20)
    paginated_query3 = builder.get_query()
    expected_pagination3 = "LIMIT 20"
    split_up = [x for x in paginated_query3.split("\n") if len(x) > 0]
    assert split_up[-1].strip() == expected_pagination3
