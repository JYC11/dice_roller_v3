from random import randint, choice

from app.domain import commands
from app.enums import enums

dice_roll_prefixes = [
    c.value for c in enums.Commands if c.value not in ["get", "upsert", "del"]
]
dice_roll_prefixes.append("")


def user_input_factory() -> dict:
    _prefix = choice(dice_roll_prefixes)
    prefix = "std" if _prefix == "" else _prefix
    multiplier = randint(1, 100)
    dice_count = randint(1, 100)
    dice_size = randint(2, 100)
    modifier = randint(-100, 100)
    threshold = randint(0, 100)
    dice_roll = f"{prefix} {multiplier}x{dice_count}d{dice_size}"
    if modifier > 0:
        dice_roll += f"+{modifier}"
    elif modifier < 0:
        dice_roll += f"-{abs(modifier)}"
    elif modifier == 0:
        dice_roll += ""
    dice_roll += f"t{threshold}"

    output = {
        "dice_roll": dice_roll,
        "expected_prefix": prefix,
        "expected_multiplier": multiplier,
        "expected_dice_count": dice_count,
        "expected_dice_size": dice_size,
        "expected_modifier": modifier,
        "expected_threshold": threshold,
    }
    return output


def roll_dice_command_factory(
    prefix: enums.Commands | None = None,
    multiplier: int | None = None,
    dice_count: int | None = None,
    dice_size: int | None = None,
    modifier: int | None = None,
    threshold: int | None = None,
):
    if not prefix:
        _prefix = choice(dice_roll_prefixes)
        prefix = "std" if _prefix == "" else _prefix
    if not multiplier:
        multiplier = randint(1, 100)
    if not dice_count:
        dice_count = randint(1, 100)
    if not dice_size:
        dice_size = randint(2, 100)
    if not modifier:
        modifier = randint(-100, 100)
    if not threshold:
        threshold = randint(0, 100)
    cmd = commands.RollDice(
        prefix=prefix,
        multiplier=multiplier,
        dice_count=dice_count,
        dice_size=dice_size,
        modifier=modifier,
        threshold=threshold,
    )
    return cmd
