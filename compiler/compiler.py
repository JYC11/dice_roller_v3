import re
from typing import Any

from enums.enums import Commands, DiceRegexes


def validator(raw_user_input: str):
    return


def extract_prefix(raw_user_input: str, command_dict: dict) -> dict:
    command = "std"
    raw_user_input = raw_user_input.lower()
    if raw_user_input.startswith(Commands.ADVANTAGE.value):
        command = Commands.ADVANTAGE.value
    elif raw_user_input.startswith(Commands.DISADVANTAGE.value):
        command = Commands.DISADVANTAGE.value
    elif raw_user_input.startswith(Commands.DROPMAX.value):
        command = Commands.DROPMAX.value
    elif raw_user_input.startswith(Commands.DROPMIN.value):
        command = Commands.DROPMIN.value
    elif raw_user_input.startswith(Commands.GETMAX.value):
        command = Commands.GETMAX.value
    elif raw_user_input.startswith(Commands.GETMIN.value):
        command = Commands.GETMIN.value
    elif raw_user_input.startswith(Commands.AVERAGE.value):
        command = Commands.AVERAGE.value
    elif raw_user_input.startswith(Commands.MAX.value):
        command = Commands.MAX.value
    elif raw_user_input.startswith(Commands.MIN.value):
        command = Commands.MIN.value
    command_dict["prefix"] = command
    return command_dict


def get_multiplier(raw_user_input: str, command_dict: dict) -> dict:
    multiplier: list[str] = re.findall(DiceRegexes.MULTIPLIER.value, raw_user_input)
    command_dict["multiplier"] = (
        int(multiplier[0].replace("x", "")) if multiplier else 1
    )
    return command_dict

def get_dice(raw_user_input: str, command_dict: dict) -> dict:
    dice: list[str] = re.findall(DiceRegexes.DICE.value, raw_user_input)
    command_dict["dice_count"] = int(dice[0].split("d")[0]) if dice else 1
    command_dict["dice_size"] = int(dice[0].split("d")[1]) if dice else 1
    return command_dict

def get_modifier(raw_user_input: str, command_dict: dict) -> dict:
    modifier: list[str] = re.findall(DiceRegexes.MODIFIER.value, raw_user_input)

    if modifier:
        if modifier[0].startswith("+"):
            modifier = int(modifier[0].replace("+", ""))
        elif modifier[0].startswith("-"):
            modifier = -int(modifier[0].replace("-", ""))
    else:
        modifier = 0

    command_dict["modifier"] = modifier
    return command_dict


def create_command_object(raw_user_input: str) -> dict:
    command_dict: dict[str, Any] = {}
    command_dict = extract_prefix(raw_user_input, command_dict)
    command_dict = get_multiplier(raw_user_input, command_dict)
    command_dict = get_dice(raw_user_input, command_dict)
    command_dict = get_modifier(raw_user_input, command_dict)
    return command_dict


def compile_raw_user_input(raw_user_input: str):
    commands: list[str] = raw_user_input.split(",")
    commands_list: list[dict] = [create_command_object(x) for x in commands]
    return commands_list