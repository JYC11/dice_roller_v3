from app.tests.factories import user_input_factory
import pytest


@pytest.fixture(scope="function")
def test_individual_raw_user_input_data() -> list[dict]:
    data = [user_input_factory() for _ in range(10)]
    return data


@pytest.fixture(scope="function")
def test_multiple_raw_user_input_data() -> list[tuple]:
    data = [(user_input_factory(), user_input_factory()) for _ in range(10)]
    return data
