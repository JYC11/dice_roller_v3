import sys
import random


from app.domain import commands, events
from app.enums import enums
from app.enums.enums import MetaCommands, MetaCommandOutputs, Commands


def do_meta_command_output(command: str) -> str:
    command = command.lower()
    if command == MetaCommands.EXIT.value:
        print(MetaCommandOutputs.EXIT.value)
        sys.exit(0)
    elif command == MetaCommands.HELP.value:
        print(MetaCommandOutputs.HELP.value)
        return MetaCommandOutputs.HELP.value
    elif command == MetaCommands.DICE.value:
        print(MetaCommandOutputs.DICE.value)
        return MetaCommandOutputs.DICE.value
    elif command == MetaCommands.PREFIX.value:
        print(MetaCommandOutputs.PREFIX.value)
        return MetaCommandOutputs.PREFIX.value


def dice_roll_handler(dice_roll: commands.RollDice):
    prefix = dice_roll.prefix
    multiplier = dice_roll.multiplier
    dice_count = dice_roll.dice_count
    dice_size = dice_roll.dice_size
    modifier = dice_roll.modifier
    dice_range = [n for n in range(1, dice_size + 1)]
    all_dice_rolls = []
    for i in range(multiplier):
        match prefix:
            case "std":
                rolls = [random.choice(dice_range) for _ in range(dice_count)]
            case Commands.ADVANTAGE.value | Commands.DISADVANTAGE.value:
                _rolls = [random.choice(dice_range) for _ in range(dice_count + 1)]
                if prefix == Commands.ADVANTAGE.value:
                    rolls = [max(_rolls)]
                elif prefix == Commands.DISADVANTAGE.value:
                    rolls = [min(_rolls)]
            case Commands.DROPMAX.value | Commands.DROPMIN.value:
                _rolls = [random.choice(dice_range) for _ in range(dice_count)]
                if prefix == Commands.DROPMAX.value:
                    _rolls.sort(reverse=True)
                elif prefix == Commands.DROPMIN.value:
                    _rolls.sort()
                rolls = _rolls[1:]
            case Commands.AVERAGE.value:
                average = float(sum(dice_range)) / float(dice_size)
                rolls = [average for _ in range(dice_count)]
            case Commands.MAX.value:
                rolls = [dice_size for _ in range(dice_count)]
            case Commands.MIN.value:
                rolls = [1 for _ in range(dice_count)]
        result = events.DiceRolled(
            roll_number=i + 1,
            dice_result=sum(rolls),
            dice_results=rolls,
            modifier=modifier,
            total=sum(rolls) + modifier,
        )
        all_dice_rolls.append(result)
    return all_dice_rolls
