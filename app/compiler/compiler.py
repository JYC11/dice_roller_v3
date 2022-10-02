import re
from typing import Any

from app.domain.commands import RollDiceCommand
from app.enums.enums import Commands, DiceRegexes, CompileValidationResults


# DICE COMPILER
def validator(raw_user_input: str) -> bool:
    dice: list[str] = re.findall(DiceRegexes.DICE.value, raw_user_input)
    if len(dice) == 0:
        return CompileValidationResults.COMPILE_IMPOSSIBLE.value
    return CompileValidationResults.COMPILE_POSSIBLE.value


def extract_prefix(raw_user_input: str) -> dict:
    prefix = "std"
    raw_user_input = raw_user_input.lower().strip()
    if raw_user_input.startswith(Commands.ADVANTAGE.value):
        prefix = Commands.ADVANTAGE.value
    elif raw_user_input.startswith(Commands.DISADVANTAGE.value):
        prefix = Commands.DISADVANTAGE.value
    elif raw_user_input.startswith(Commands.DROPMAX.value):
        prefix = Commands.DROPMAX.value
    elif raw_user_input.startswith(Commands.DROPMIN.value):
        prefix = Commands.DROPMIN.value
    elif raw_user_input.startswith(Commands.GETMAX.value):
        prefix = Commands.GETMAX.value
    elif raw_user_input.startswith(Commands.GETMIN.value):
        prefix = Commands.GETMIN.value
    elif raw_user_input.startswith(Commands.AVERAGE.value):
        prefix = Commands.AVERAGE.value
    elif raw_user_input.startswith(Commands.MAX.value):
        prefix = Commands.MAX.value
    elif raw_user_input.startswith(Commands.MIN.value):
        prefix = Commands.MIN.value
    elif raw_user_input.startswith(Commands.THRESH.value):
        prefix = Commands.THRESH.value
    return prefix


def get_multiplier(raw_user_input: str) -> int:
    multiplier: list[str] = re.findall(DiceRegexes.MULTIPLIER.value, raw_user_input)
    return int(multiplier[0].replace("x", "")) if multiplier else 1


def get_dice(raw_user_input: str) -> tuple[int, int]:
    dice: list[str] = re.findall(DiceRegexes.DICE.value, raw_user_input)
    dice_count = int(dice[0].split("d")[0]) if dice else 1
    dice_size = int(dice[0].split("d")[1]) if dice else 1
    return dice_count, dice_size


def get_modifier(raw_user_input: str) -> int:
    modifier: list[str] = re.findall(DiceRegexes.MODIFIER.value, raw_user_input)

    if modifier:
        if modifier[0].startswith("+"):
            modifier = int(modifier[0].replace("+", ""))
        elif modifier[0].startswith("-"):
            modifier = -int(modifier[0].replace("-", ""))
    else:
        modifier = 0

    return modifier


def create_roll_dice_command(raw_user_input: str) -> RollDiceCommand:
    prefix = extract_prefix(raw_user_input)
    multiplier = get_multiplier(raw_user_input)
    dice_count, dice_size = get_dice(raw_user_input)
    modifier = get_modifier(raw_user_input)
    return RollDiceCommand(
        prefix=prefix,
        multiplier=multiplier,
        dice_count=dice_count,
        dice_size=dice_size,
        modifier=modifier,
    )


def compile_raw_user_input(raw_user_input: str) -> list[RollDiceCommand]:
    commands: list[str] = raw_user_input.split(",")
    commands_list: list[RollDiceCommand] = [
        create_roll_dice_command(x) for x in commands
    ]
    return commands_list


# TODO
# CHARACTER COMPILER
