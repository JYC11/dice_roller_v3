from .base import Base
from enums import enums

from collections import deque
from dataclasses import field

from app.service.handler import dice_roll_handler


class DndCharcter(Base):
    name: str
    class_name: str
    subclass_name: str
    strength_mod: int
    dexterity_mod: int
    consitution_mod: int
    intelligence_mod: int
    wisdom_mod: int
    charisma_mod: int
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

    def _construct_attack_roll(self):
        return

    def _construct_damage_roll(self):
        return

    def _construct_skill_check_roll(self):
        return

    def _construct_saving_throw_roll(self):
        return

    def make_attack_roll(self):
        return

    def make_damage_roll(self):
        return

    def make_skill_check(self):
        return

    def make_saving_throw(self):
        return


class DndAttacks(Base):  # look into things that give advantage
    name: str
    weapon_type: enums.DndWeapons
    item_bonus: int
    finesse: bool
    class_bonus: int
    subclass_bonus: int
    feature_bonus: int
    crit_range: int = 20
    damage: "DndDamage"


class DndDamage(Base):
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
