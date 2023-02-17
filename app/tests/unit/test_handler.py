from app.enums import enums
from app.service.handler import roll_dice
from app.tests.factories.input import (
    roll_dice_command_factory,
    dnd_full_character_factory,
)


def test_roll_dice():
    for _ in range(10):
        cmd = roll_dice_command_factory(
            prefix=enums.Commands.DISADVANTAGE.value, multiplier=3, dice_count=1
        )
        results = roll_dice(cmd)
        for result in results:
            assert len(result.dropped_rolls) == 1

    for _ in range(10):
        cmd = roll_dice_command_factory(
            prefix=enums.Commands.ADVANTAGE.value, multiplier=3, dice_count=1
        )
        results = roll_dice(cmd)
        for result in results:
            assert len(result.dropped_rolls) == 1

    for _ in range(10):
        cmd = roll_dice_command_factory(prefix=enums.Commands.DROPMAX.value)
        results = roll_dice(cmd)
        for result in results:
            assert len(result.dropped_rolls) == 1

    for _ in range(10):
        cmd = roll_dice_command_factory(prefix=enums.Commands.DROPMIN.value)
        results = roll_dice(cmd)
        for result in results:
            assert len(result.dropped_rolls) == 1

    for _ in range(10):
        cmd = roll_dice_command_factory(
            prefix=enums.Commands.THRESH.value, dice_size=100, threshold=50
        )
        results = roll_dice(cmd)
        for result in results:
            assert len(result.lower_rolls) >= 0


def test_create_dice_commands():
    chars = dnd_full_character_factory()
    character = chars[0]
    assert character
    attack_name = character.attacks[0].name
    skill_name = character.skill_proficiencies[0]
    saving_throw = character.saving_throw_proficiencies[0]
    attack_roll = character.construct_attack_roll(attack_name)
    skill_roll = character.construct_skill_check_roll(skill_name)
    saving_throw_roll = character.construct_saving_throw_roll(saving_throw)
    assert attack_roll
    assert skill_roll
    assert saving_throw_roll
    results = roll_dice(attack_roll)
    assert results
    damage_roll = character.construct_damage_roll(
        attack_result=results[0],
        use_two_hands=False,
        use_dual_wielding=False,
        attack_name=attack_name,
    )
    assert damage_roll
