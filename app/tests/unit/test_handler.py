from app.enums import enums
from app.service.handler import roll_dice
from app.tests.factories import roll_dice_command_factory


def test_roll_dice():
    for _ in range(10):
        cmd = roll_dice_command_factory(
            prefix=enums.Commands.DISADVANTAGE.value, multiplier=3, dice_count=1
        )
        results = roll_dice(cmd)
        for result in results:
            assert len(result.dropped_roll) == 1

    for _ in range(10):
        cmd = roll_dice_command_factory(
            prefix=enums.Commands.ADVANTAGE.value, multiplier=3, dice_count=1
        )
        results = roll_dice(cmd)
        for result in results:
            assert len(result.dropped_roll) == 1

    for _ in range(10):
        cmd = roll_dice_command_factory(prefix=enums.Commands.DROPMAX.value)
        results = roll_dice(cmd)
        for result in results:
            assert len(result.dropped_roll) == 1

    for _ in range(10):
        cmd = roll_dice_command_factory(prefix=enums.Commands.DROPMIN.value)
        results = roll_dice(cmd)
        for result in results:
            assert len(result.dropped_roll) == 1

    for _ in range(10):
        cmd = roll_dice_command_factory(
            prefix=enums.Commands.THRESH.value, dice_size=100, threshold=50
        )
        results = roll_dice(cmd)
        for result in results:
            assert len(result.dropped_roll) >= 0
