from app.compiler import compiler
from app.domain.commands import RollDice


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


def test_get_threshold(test_individual_raw_user_input_data: list[dict]):
    for test_data in test_individual_raw_user_input_data:
        assert (
            compiler.get_threshold(test_data["dice_roll"])
            == test_data["expected_threshold"]
        )


def test_create_roll_dice_command(test_individual_raw_user_input_data: list[dict]):
    for test_data in test_individual_raw_user_input_data:
        expected = RollDice(
            game_type="dnd",
            prefix=test_data["expected_prefix"],
            multiplier=test_data["expected_multiplier"],
            dice_count=test_data["expected_dice_count"],
            dice_size=test_data["expected_dice_size"],
            modifier=test_data["expected_modifier"],
            threshold=test_data["expected_threshold"],
        )
        actual = compiler.create_roll_dice_command(test_data["dice_roll"])
        assert type(actual) == RollDice
        assert expected == actual


def test_compile_raw_user_input(test_multiple_raw_user_input_data: list[tuple]):
    for test_data in test_multiple_raw_user_input_data:
        data1, data2 = test_data
        command1 = RollDice(
            game_type="dnd",
            prefix=data1["expected_prefix"],
            multiplier=data1["expected_multiplier"],
            dice_count=data1["expected_dice_count"],
            dice_size=data1["expected_dice_size"],
            modifier=data1["expected_modifier"],
            threshold=data1["expected_threshold"],
        )
        command2 = RollDice(
            game_type="dnd",
            prefix=data2["expected_prefix"],
            multiplier=data2["expected_multiplier"],
            dice_count=data2["expected_dice_count"],
            dice_size=data2["expected_dice_size"],
            modifier=data2["expected_modifier"],
            threshold=data2["expected_threshold"],
        )
        expected = [command1, command2]

        dice_roll1 = data1["dice_roll"]
        dice_roll2 = data2["dice_roll"]
        input_str = f"{dice_roll1}, {dice_roll2}"
        actual = compiler.compile_raw_user_input(input_str)
        assert expected == actual
