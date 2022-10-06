from collections import deque
from dataclasses import field
from typing import Optional

from .base import Base
from app.enums import enums
from app.domain import commands, events
from app.utils.binary_search import binary_search
from app.utils.data import constants
from app.domain import exceptions as domain_exc


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
    character_events: deque = field(default_factory=deque)

    @property
    def _attack_dict(self) -> dict[str, "DndAttacks"]:
        res = {x.name: x for x in self.attacks}
        return res

    def construct_damage_roll(
        self,
        attack_result: events.DiceRolled,
        use_two_hands: bool = False,
        use_dual_wielding: bool = False,
        attack_name: str = None,
        prefix: enums.Commands | str = "std",
        additional_dice_count: int = 0,
        additional_dice_size: int = 0,
    ) -> commands.RollDice:
        attack: Optional[DndAttacks] = self._attack_dict.get(attack_name)
        if not attack:
            raise domain_exc.AttackNameNotFound(
                f"attack with name {attack_name} not found"
            )
        damage: DndDamage = attack.damage
        dice_count = damage.dice_count
        if attack_result.critical:
            dice_count *= damage.crit_dice_multiplier
            dice_count += damage.additional_crit_dice

        if damage.versatile and use_two_hands:
            dice_size = damage.two_hand_dice_size
        else:
            dice_size = damage.dice_size

        modifier = 0

        if not use_dual_wielding:
            if attack.finesse:
                dex_mod = constants.ability_scores_and_modifiers.get(self.dexterity)
                assert dex_mod is not None
                modifier += dex_mod
            else:
                str_mod = constants.ability_scores_and_modifiers.get(self.strength)
                assert str_mod is not None
                modifier += str_mod

        modifier += (
            damage.class_bonus
            + damage.subclass_bonus
            + damage.feature_bonus
            + damage.item_bonus
        )

        cmd = commands.RollDice(
            game_type=enums.GameType.DND.value,
            prefix=prefix,
            multiplier=1,
            dice_count=dice_count,
            dice_size=dice_size,
            modifier=modifier,
            crit_threshold=attack.crit_threshold,
        )
        return cmd

    def construct_attack_roll(
        self,
        attack_name: str = None,
        prefix: enums.Commands | str = "std",
    ) -> commands.RollDice:
        attack: Optional[DndAttacks] = self._attack_dict.get(attack_name)
        if not attack:
            raise domain_exc.AttackNameNotFound(
                f"attack with name {attack_name} not found"
            )

        modifier = 0
        if attack.finesse:
            dex_mod = constants.ability_scores_and_modifiers.get(self.dexterity)
            assert dex_mod is not None
            modifier += dex_mod
        else:
            str_mod = constants.ability_scores_and_modifiers.get(self.strength)
            assert str_mod is not None
            modifier += str_mod

        if attack.weapon_type in self.weapon_proficiencies:
            modifier += self.proficiency

        modifier += (
            attack.item_bonus
            + attack.feature_bonus
            + attack.class_bonus
            + attack.subclass_bonus
        )
        cmd = commands.RollDice(
            game_type=enums.GameType.DND.value,
            prefix=prefix,
            multiplier=1,
            dice_count=1,
            dice_size=20,
            modifier=modifier,
            crit_threshold=attack.crit_threshold,
        )
        return cmd

    def construct_skill_check_roll(
        self,
        skill: enums.DndSkills,
        extra: int = 0,
        prefix: Optional[enums.Commands] = None,
    ) -> commands.RollDice:
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
            game_type=enums.GameType.DND.value,
            prefix=prefix,
            multiplier=1,
            dice_count=1,
            dice_size=20,
            modifier=modifier,
            crit_threshold=20,
        )
        return cmd

    def construct_saving_throw_roll(
        self,
        ability: str,
        extra: int = 0,
        prefix: Optional[enums.Commands] = None,
    ) -> commands.RollDice:
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
            game_type=enums.GameType.DND.value,
            prefix=prefix,
            multiplier=1,
            dice_count=1,
            dice_size=20,
            modifier=modifier,
            crit_threshold=20,
        )
        return cmd


class DndAttacks(Base):  # look into things that give advantage
    character_id: int  # fk
    name: str
    weapon_type: enums.DndWeapons
    item_bonus: int
    finesse: bool
    class_bonus: int
    subclass_bonus: int
    feature_bonus: int
    crit_threshold: int = 20
    damage: list["DndDamage"]


class DndDamage(Base):
    attack_id: int  # fk
    name: str
    dice_count: int
    dice_size: int
    two_hand_dice_size: int
    damage_type: str
    versatile: bool
    weight: enums.DndWeaponWeight = enums.DndWeaponWeight.MEDIUM.value
    crit_dice_multiplier: bool = 2
    additional_crit_dice: int = 0
    item_bonus: int
    class_bonus: int
    subclass_bonus: int
    feature_bonus: int
    rerolls_ones: bool
    range: int
