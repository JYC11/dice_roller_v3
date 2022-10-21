import random

import factory
from sqlalchemy.orm import Session
from faker import Faker

from app.common.db import SessionLocal
from app.domain.models import DndCharacter, DndAttack, DndDamage
from app.enums import enums

fake = Faker()


class DndCharacterFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = DndCharacter
        assert SessionLocal is not None
        sqlalchemy_session = SessionLocal()
        sqlalchemy_session_persistence = "commit"

    name: str = factory.Faker("name")
    level: int = factory.Faker("random_int", min=1, max=20)
    hp: int = factory.Faker("random_int", min=1, max=200)
    race: str = factory.Faker("word")
    background: str = factory.Faker("word")
    class_info: str = factory.Faker("word")
    strength: int = factory.Faker("random_int", min=1, max=20)
    dexterity: int = factory.Faker("random_int", min=1, max=20)
    constitution: int = factory.Faker("random_int", min=1, max=20)
    intelligence: int = factory.Faker("random_int", min=1, max=20)
    wisdom: int = factory.Faker("random_int", min=1, max=20)
    charisma: int = factory.Faker("random_int", min=1, max=20)
    hit_dice: str = factory.Faker("numerify", "d#")
    proficiency: int = factory.Faker("random_int", min=1, max=5)
    armour_class: int = factory.Faker("random_int", min=1, max=20)
    # weapon_proficiencies: list[enums.DndWeapons]
    # saving_throw_proficiencies: list[enums.DndAbilities]
    # skill_proficiencies: list[enums.DndSkills]
    # skill_expertises: list[enums.DndSkills]
    # tool_proficiencies: list[enums.DndTools]
    # tool_expertises: list[enums.DndTools]
    # attacks: list["DndAttack"]
