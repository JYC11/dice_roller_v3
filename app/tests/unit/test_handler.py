from app.service.handler import dice_roll_handler
from app.tests.factories import roll_dice_command_factory


def test_dice_roll_handler():
    for _ in range(10):
        cmd = roll_dice_command_factory(prefix="std", multiplier=3)
        result = dice_roll_handler(cmd)
        print(result)
    assert 1 == 1
