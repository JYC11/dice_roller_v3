import sys
import random


from app.domain import commands, events
from app.service import exceptions
from app.enums import enums


def do_meta_command_output(command: str) -> str:
    command = command.lower()
    if command == enums.MetaCommands.EXIT.value:
        print(enums.MetaCommandOutputs.EXIT.value)
        sys.exit(0)
    elif command == enums.MetaCommands.HELP.value:
        print(enums.MetaCommandOutputs.HELP.value)
        return enums.MetaCommandOutputs.HELP.value
    elif command == enums.MetaCommands.DICE.value:
        print(enums.MetaCommandOutputs.DICE.value)
        return enums.MetaCommandOutputs.DICE.value
    elif command == enums.MetaCommands.PREFIX.value:
        print(enums.MetaCommandOutputs.PREFIX.value)
        return enums.MetaCommandOutputs.PREFIX.value


def dice_roll_handler(dice_roll: commands.RollDice) -> list[events.DiceRolled]:
    prefix = dice_roll.prefix
    multiplier = dice_roll.multiplier
    dice_count = dice_roll.dice_count
    dice_size = dice_roll.dice_size
    modifier = dice_roll.modifier
    dice_range = [n for n in range(1, dice_size + 1)]
    all_dice_rolls: list[events.DiceRolled] = []
    for i in range(multiplier):
        dropped_roll = []
        match prefix:
            case "std":
                rolls = [random.choice(dice_range) for _ in range(dice_count)]
            case enums.Commands.ADVANTAGE.value | enums.Commands.DISADVANTAGE.value:
                if dice_count > 1:
                    raise exceptions.IncorrectDiceCount
                _rolls = [random.choice(dice_range) for _ in range(dice_count + 1)]
                if prefix == enums.Commands.ADVANTAGE.value:
                    rolls = [max(_rolls)]
                    dropped_roll.append(min(_rolls))
                elif prefix == enums.Commands.DISADVANTAGE.value:
                    rolls = [min(_rolls)]
                    dropped_roll.append(max(_rolls))
            case enums.Commands.DROPMAX.value | enums.Commands.DROPMIN.value:
                _rolls = [random.choice(dice_range) for _ in range(dice_count)]
                if prefix == enums.Commands.DROPMAX.value:
                    _rolls.sort(reverse=True)
                elif prefix == enums.Commands.DROPMIN.value:
                    _rolls.sort()
                rolls = _rolls[1:]
                dropped_roll.append(_rolls[0])
            case enums.Commands.AVERAGE.value:
                average = float(sum(dice_range)) / float(dice_size)
                rolls = [average for _ in range(dice_count)]
            case enums.Commands.MAX.value:
                rolls = [dice_size for _ in range(dice_count)]
            case enums.Commands.MIN.value:
                rolls = [1 for _ in range(dice_count)]
            case enums.Commands.REROLL_ONES.value:
                _rolls = [random.choice(dice_range) for _ in range(dice_count)]
                _rolls.sort()
                if _rolls[0] == 1:
                    rolls = _rolls[1:]
                    rolls.append(random.choice(dice_range))
                else:
                    rolls = _rolls
            case enums.Commands.THRESH.value:
                threshold = dice_roll.threshold
                if not threshold:
                    raise exceptions.ThresholdNotProvided
                _rolls = [random.choice(dice_range) for _ in range(dice_count)]
                rolls = [x for x in _rolls if x >= dice_roll.threshold]
                lower_rolls = [x for x in _rolls if x < dice_roll.threshold]
                dropped_roll.extend(lower_rolls)
        result = events.DiceRolled(
            roll_number=i + 1,
            dice_result=sum(rolls),
            dice_results=rolls,
            modifier=modifier,
            total=sum(rolls) + modifier,
            dropped_roll=dropped_roll,
        )
        all_dice_rolls.append(result)
    return all_dice_rolls
