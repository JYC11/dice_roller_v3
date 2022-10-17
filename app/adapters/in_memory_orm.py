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
    event,
)
from sqlalchemy.orm import mapper, relationship

from domain import models

logger = logging.getLogger(__name__)

metadata = MetaData()

dnd_characters = Table(
    "dnd_characters",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("create_dt", DateTime),
    Column("update_dt", DateTime),
    Column("name", String(255), nullable=False),
    Column("level", Integer, nullable=False),
    Column("strength", Integer, nullable=False),
    Column("dexterity", Integer, nullable=False),
    Column("constitution", Integer, nullable=False),
    Column("intelligence", Integer, nullable=False),
    Column("wisdom", Integer, nullable=False),
    Column("charisma", Integer, nullable=False),
    Column("hit_dice", Integer, nullable=False),
    Column("proficiency", Integer, nullable=False),
    Column("armour_class", Integer, nullable=False),
)


dnd_attacks = Table(
    "dnd_attacks",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("create_dt", DateTime),
    Column("update_dt", DateTime),
    Column("character_id", ForeignKey("dnd_character.id"), nullable=False),
    Column("name", String(255), nullable=False),
    Column("weapon_type", Integer, nullable=False),
    Column("item_bonus", Integer, nullable=False),
    Column("finesse", Boolean, nullable=False),
    Column("class_bonus", Integer, nullable=False),
    Column("subclass_bonus", Integer, nullable=False),
    Column("feature_bonus", Integer, nullable=False),
    Column("crit_threshold", Integer, nullable=False, default=20),
    Column("damage_id", ForeignKey("dnd_damage.id"), nullable=False),
)

dnd_damages = Table(
    "dnd_damages",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("create_dt", DateTime),
    Column("update_dt", DateTime),
    Column("attack_id", ForeignKey("dnd_attack.id"), nullable=False),
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
)


def start_mappers():
    logger.info("Starting mappers")
    mapper(
        models.DndCharacter,
        dnd_characters,
        properties={"attacks": relationship(models.DndAttack)},
    )
    mapper(
        models.DndAttack,
        dnd_attacks,
        properties={"character": relationship(models.DndCharacter)},
        properties={"damage": relationship(models.DndDamage)},
    )
    mapper(
        models.DndDamage,
        dnd_damages,
        properties={"attack": relationship(models.DndAttack)},
    )
