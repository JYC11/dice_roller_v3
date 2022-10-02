from app.compiler import compiler
from app.domain.commands import RollDice


def test_create_roll_dice_command(test_individual_raw_user_input_data: list[dict]):
    for test_data in test_individual_raw_user_input_data:
        expected = RollDice(
            prefix=test_data["expected_prefix"],
            multiplier=test_data["expected_multiplier"],
            dice_count=test_data["expected_dice_count"],
            dice_size=test_data["expected_dice_size"],
            modifier=test_data["expected_modifier"],
        )
        actual = compiler.create_roll_dice_command(test_data["dice_roll"])
        assert type(actual) == RollDice
        assert expected == actual


def test_compile_raw_user_input(test_multiple_raw_user_input_data: list[tuple]):
    for test_data in test_multiple_raw_user_input_data:
        data1, data2 = test_data
        command1 = RollDice(
            prefix=data1["expected_prefix"],
            multiplier=data1["expected_multiplier"],
            dice_count=data1["expected_dice_count"],
            dice_size=data1["expected_dice_size"],
            modifier=data1["expected_modifier"],
        )
        command2 = RollDice(
            prefix=data2["expected_prefix"],
            multiplier=data2["expected_multiplier"],
            dice_count=data2["expected_dice_count"],
            dice_size=data2["expected_dice_size"],
            modifier=data2["expected_modifier"],
        )
        expected = [command1, command2]

        dice_roll1 = data1["dice_roll"]
        dice_roll2 = data2["dice_roll"]
        input_str = f"{dice_roll1}, {dice_roll2}"
        actual = compiler.compile_raw_user_input(input_str)
        assert expected == actual
