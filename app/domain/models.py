from collections import deque
from dataclasses import field
from typing import Optional

from .base import Base
from app.enums import enums
from app.domain import commands
from app.utils.binary_search import binary_search
from app.utils.data import constants
from app.service.handler import dice_roll_handler


class DndCharcter(Base):
    name: str
    class_name: str
    subclass_name: str
    strength: int
    dexterity: int
    consitution: int
    intelligence: int
    wisdom: int
    charisma: int
    hit_dice: int
    hit_dice_count: int
    proficiency: int
    armour_class: int
    weapon_proficiencies: list[enums.DndWeapons]
    saving_throw_proficiencies: list[enums.DndAbilities]
    skill_proficiencies: list[enums.DndSkills]
    skill_expertises: list[enums.DndSkills]
    tool_proficiencies: list[enums.DndTools]
    tool_expertises: list[enums.DndTools]
    attacks: list["DndAttacks"]
    events: deque = field(default_factory=deque)

    def make_attack_roll(
        self,
        attack_name: Optional[str] = None,
        attack_id: Optional[int] = None,
    ):
        return

    def make_damage_roll(
        self,
        attack_name: Optional[str] = None,
        attack_id: Optional[int] = None,
    ):
        return

    def make_skill_check_roll(
        self, skill: enums.DndSkills, extra: int = 0, prefix: Optional[str] = None
    ):
        modifier = 0
        modifier += extra
        ability_name = constants.skills_and_abilities.get(skill)
        ability_score = getattr(self, ability_name)
        ability_mod = constants.ability_scores_and_modifiers.get(ability_score)
        modifier += ability_mod

        if binary_search(self.skill_proficiencies, skill):
            modifier += self.proficiency
        if binary_search(self.skill_expertises, skill):
            modifier += self.proficiency
        if not prefix:
            prefix = "std"
        cmd = commands.RollDice(
            prefix=prefix,
            multiplier=1,
            dice_count=1,
            dice_size=20,
            modifier=modifier,
        )
        result = dice_roll_handler(cmd)
        return result

    def make_saving_throw_roll(
        self, ability: str, extra: int = 0, prefix: Optional[str] = None
    ):
        modifier = 0
        modifier += extra
        ability_score = getattr(self, ability)
        ability_mod = constants.ability_scores_and_modifiers.get(ability_score)
        modifier += ability_mod

        if binary_search(self.saving_throw_proficiencies, ability):
            modifier += self.proficiency
        if not prefix:
            prefix = "std"
        cmd = commands.RollDice(
            prefix=prefix,
            multiplier=1,
            dice_count=1,
            dice_size=20,
            modifier=modifier,
        )
        result = dice_roll_handler(cmd)
        return result


class DndAttacks(Base):  # look into things that give advantage
    character_id: int  # fk
    name: str
    weapon_type: enums.DndWeapons
    item_bonus: int
    finesse: bool
    class_bonus: int
    subclass_bonus: int
    feature_bonus: int
    crit_range: int = 20
    damage: list["DndDamage"]


class DndDamage(Base):
    attack_id: int  # fk
    name: str
    dice_count: int
    dice_size: int
    damage_type: str
    one_hand: bool
    two_hand: bool
    dual_wielding: bool
    crit: bool
    additional_crit_dice: int
    item_bonus: int
    class_bonus: int
    subclass_bonus: int
    feature_bonus: int
    rerolls_ones: bool
