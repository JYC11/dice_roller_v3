from datetime import datetime
from random import randint, choice, sample

from app.domain import models
from app.domain import commands
from app.enums import enums

from faker import Faker

fake = Faker()

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
    game_type: enums.GameType | None = None,
    prefix: enums.Commands | None = None,
    multiplier: int | None = None,
    dice_count: int | None = None,
    dice_size: int | None = None,
    modifier: int | None = None,
    threshold: int | None = None,
):
    if not game_type:
        game_type = enums.GameType.DND.value
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
        game_type=game_type,
        prefix=prefix,
        multiplier=multiplier,
        dice_count=dice_count,
        dice_size=dice_size,
        modifier=modifier,
        threshold=threshold,
    )
    return cmd


def dnd_character_factory(id) -> models.DndCharacter:
    character = models.DndCharacter()
    character.id = id
    character.create_dt = datetime.now()
    character.name = fake.name()
    character.level = (randint(1, 20),)
    character.strength = randint(1, 20)
    character.dexterity = randint(1, 20)
    character.constitution = randint(1, 20)
    character.intelligence = randint(1, 20)
    character.wisdom = randint(1, 20)
    character.charisma = randint(1, 20)
    character.hit_dice = randint(6, 12)
    character.proficiency = randint(2, 6)
    character.armour_class = randint(10, 30)
    weapon_prof_count = randint(1, 3)
    character.weapon_proficiencies = sample(
        [x.value for x in enums.DndWeapons], weapon_prof_count
    )
    saving_throw_count = randint(2, 6)
    character.saving_throw_proficiencies = sample(
        [x.value for x in enums.DndAbilities], saving_throw_count
    )
    skill_prof_count = randint(2, 6)
    character.skill_proficiencies = sample(
        [x.value for x in enums.DndSkills], skill_prof_count
    )
    skill_expertise_count = randint(0, 3)
    character.skill_expertises = sample(
        character.skill_proficiencies, skill_expertise_count
    )
    tool_prof_count = randint(2, 6)
    character.tool_proficiencies = sample(
        [x.value for x in enums.DndTools], tool_prof_count
    )
    tool_expertise_count = randint(0, 3)
    character.tool_expertises = sample(
        character.tool_proficiencies, tool_expertise_count
    )
    return character


def dnd_attack_factory(character_id: int) -> models.DndAttack:
    attack = models.DndAttack()
    attack.character_id = character_id
    attack.name = fake.word()
    attack.weapon_type = choice([x.value for x in enums.DndWeapons])
    attack.item_bonus = randint(0, 3)
    attack.finesse = choice([True, False])
    attack.class_bonus = randint(0, 10)
    attack.subclass_bonus = randint(0, 10)
    attack.feature_bonus = randint(0, 10)
    attack.crit_threshold = 20
    return attack


def dnd_damage_factory(attack_id: int) -> models.DndDamage:
    damage = models.DndDamage()
    damage.attack_id = attack_id
    damage.name = fake.word()
    damage.dice_count = randint(1, 5)
    damage.dice_size = randint(6, 12)
    damage.two_hand_dice_size = randint(8, 12)
    damage.damage_type = fake.word()
    damage.versatile = choice([True, False])
    damage.weight = choice([x.value for x in enums.DndWeaponWeight])
    damage.crit_dice_multiplier = 2
    damage.additional_crit_dice = randint(0, 2)
    damage.item_bonus = randint(0, 3)
    damage.class_bonus = randint(0, 10)
    damage.subclass_bonus = randint(0, 10)
    damage.feature_bonus = randint(0, 10)
    damage.rerolls_ones = choice([True, False])
    damage.range = randint(60, 120)
    return damage


def dnd_full_character_factory(count: int = 1) -> list[models.DndCharacter]:
    characters: list[models.DndCharacter] = []
    for i in range(count):
        id = i + 1
        character = dnd_character_factory(id)
        attack = dnd_attack_factory(id)
        damage = dnd_damage_factory(id)
        attack.damage = damage
        character.attacks = [attack]
        characters.append(character)
    return characters
