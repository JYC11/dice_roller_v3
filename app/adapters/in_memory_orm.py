import logging
from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    Boolean,
    DateTime,
    ForeignKey,
    # event,
)
from sqlalchemy.orm import registry, relationship

from app.domain import models
from app.adapters.type_adapters import StringifiedArray


logger = logging.getLogger(__name__)

metadata = MetaData()

mapper_registry = registry(metadata=metadata)

dnd_characters = Table(
    "dnd_characters",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("create_dt", DateTime),
    Column("update_dt", DateTime),
    Column("name", String(255), nullable=False),
    Column("level", Integer, nullable=False, default=1),
    Column("hp", Integer, nullable=False, default=1),
    Column("race", String(255), nullable=False),
    Column("background", String(255), nullable=False),
    Column("class_info", String(255), nullable=False),
    Column("strength", Integer, nullable=False, default=1),
    Column("dexterity", Integer, nullable=False, default=1),
    Column("constitution", Integer, nullable=False, default=1),
    Column("intelligence", Integer, nullable=False, default=1),
    Column("wisdom", Integer, nullable=False, default=1),
    Column("charisma", Integer, nullable=False, default=1),
    Column("hit_dice", String(255), nullable=False),
    Column("proficiency", Integer, nullable=False),
    Column("armour_class", Integer, nullable=False),
    Column("weapon_proficiencies", StringifiedArray, default=[]),
    Column("saving_throw_proficiencies", StringifiedArray, default=[]),
    Column("skill_proficiencies", StringifiedArray, default=[]),
    Column("skill_expertises", StringifiedArray, default=[]),
    Column("tool_proficiencies", StringifiedArray, default=[]),
    Column("tool_expertises", StringifiedArray, default=[]),
)


dnd_attacks = Table(
    "dnd_attacks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("create_dt", DateTime),
    Column("update_dt", DateTime),
    Column("name", String(255), nullable=False),
    Column("weapon_type", Integer, nullable=False),
    Column("item_bonus", Integer, nullable=False),
    Column("finesse", Boolean, nullable=False),
    Column("class_bonus", Integer, nullable=False),
    Column("subclass_bonus", Integer, nullable=False),
    Column("feature_bonus", Integer, nullable=False),
    Column("crit_threshold", Integer, nullable=False, default=20),
    Column("character_id", Integer, ForeignKey("dnd_characters.id"), nullable=False),
    Column("damage_id", Integer, nullable=False, foreign_keys="dnd_damages.id"),
)

dnd_damages = Table(
    "dnd_damages",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("create_dt", DateTime),
    Column("update_dt", DateTime),
    Column("name", String(255), nullable=False),
    Column("dice_count", Integer, nullable=False),
    Column("dice_size", Integer, nullable=False),
    Column("two_hand_dice_size", Integer, nullable=False),
    Column("damage_type", String(255), nullable=False),
    Column("versatile", Boolean, nullable=False),
    Column("weight", String(255), nullable=False),
    Column("crit_dice_multiplier", Integer, nullable=False, default=2),
    Column("additional_crit_dice", Integer, nullable=False, default=0),
    Column("class_bonus", Integer, nullable=False),
    Column("subclass_bonus", Integer, nullable=False),
    Column("feature_bonus", Integer, nullable=False),
    Column("reroll_ones", Boolean, nullable=False),
    Column("range", Integer, nullable=False),
    Column("attack_id", Integer, ForeignKey("dnd_attacks.id"), nullable=False),
)


def start_mappers():
    logger.info("Starting mappers")
    mapper_registry.map_imperatively(
        models.DndCharacter,
        dnd_characters,
        properties={"attacks": relationship(models.DndAttack)},
    )
    mapper_registry.map_imperatively(
        models.DndAttack,
        dnd_attacks,
        properties={
            "character": relationship(models.DndCharacter, back_populates="attacks"),
            "damage": relationship(models.DndDamage),
        },
    )
    mapper_registry.map_imperatively(
        models.DndDamage,
        dnd_damages,
        properties={"attack": relationship(models.DndAttack)},
    )
