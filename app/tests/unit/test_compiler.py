from app.compiler import compiler


def test_extract_prefix(test_individual_raw_user_input_data: list[dict]):
    for test_data in test_individual_raw_user_input_data:
        assert (
            compiler.extract_prefix(test_data["dice_roll"])
            == test_data["expected_prefix"]
        )


def test_get_multiplier(test_individual_raw_user_input_data: list[dict]):
    for test_data in test_individual_raw_user_input_data:
        assert (
            compiler.get_multiplier(test_data["dice_roll"])
            == test_data["expected_multiplier"]
        )


def test_get_dice(test_individual_raw_user_input_data: list[dict]):
    for test_data in test_individual_raw_user_input_data:
        assert compiler.get_dice(test_data["dice_roll"]) == (
            test_data["expected_dice_count"],
            test_data["expected_dice_size"],
        )


def test_get_modifier(test_individual_raw_user_input_data: list[dict]):
    for test_data in test_individual_raw_user_input_data:
        assert (
            compiler.get_modifier(test_data["dice_roll"])
            == test_data["expected_modifier"]
        )
