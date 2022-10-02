from app.enums.enums import Commands
from random import randint, choice

dice_roll_prefixes = [
    c.value for c in Commands if c.value not in ["get", "upsert", "del"]
]


def user_input_generator() -> dict:
    prefix = choice(dice_roll_prefixes)
    multiplier = randint(1, 100)
    dice_count = randint(1, 100)
    dice_size = randint(2, 100)
    plus_or_minus = choice(["+", "-"])
    modifier = randint(0, 100)
    dice_roll = f"{prefix} {multiplier}x{dice_count}d{dice_size}"

    output = {
        "expected_prefix": prefix,
        "expected_multiplier": multiplier,
        "expected_dice_count": dice_count,
        "expected_dice_size": dice_size,
    }

    if plus_or_minus == "+":
        dice_roll += f"+{modifier}"
        output["expected_modifier"] = modifier
    elif plus_or_minus == "-":
        dice_roll += f"-{modifier}"
        output["expected_modifier"] = -modifier

    output["dice_roll"] = dice_roll
    return output
