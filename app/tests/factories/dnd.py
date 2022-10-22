import random

import factory
from sqlalchemy.orm import Session
from faker import Faker

from app.common.db import SessionLocal
from app.domain.models import DndCharacter, DndAttack, DndDamage
from app.enums import enums

fake = Faker()


class DndAttackFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = DndAttack
        assert SessionLocal is not None
        sqlalchemy_session = SessionLocal()
        sqlalchemy_session_persistence = "commit"

    name: str = factory.Faker("word")
    weapon_type: enums.DndWeapons = factory.LazyFunction(
        lambda: random.choice(list(enums.DndWeapons)).value
    )
    item_bonus: int = factory.Faker("random_int", min=0, max=3)
    finesse: bool = factory.Faker("boolean")
    class_bonus: int = factory.Faker("random_int", min=0, max=3)
    subclass_bonus: int = factory.Faker("random_int", min=0, max=3)
    feature_bonus: int = factory.Faker("random_int", min=0, max=3)
    crit_threshold: int = 20
    character_id: int  # fk


class DndDamageFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = DndDamage
        assert SessionLocal is not None
        sqlalchemy_session = SessionLocal()
        sqlalchemy_session_persistence = "commit"

    name: str = factory.Faker("word")
    dice_count: int = factory.Faker("random_int", min=1, max=4)
    dice_size: int = factory.Faker("random_int", min=4, max=8)
    two_hand_dice_size: int = factory.Faker("random_int", min=8, max=12)
    damage_type: str = factory.Faker("word")
    versatile: bool = factory.Faker("boolean")
    weight: enums.DndWeaponWeight = factory.LazyFunction(
        lambda: random.choice(list(enums.DndWeaponWeight)).value
    )
    crit_dice_multiplier: bool = 2
    additional_crit_dice: int = 0
    item_bonus: int = factory.Faker("random_int", min=0, max=3)
    class_bonus: int = factory.Faker("random_int", min=0, max=3)
    subclass_bonus: int = factory.Faker("random_int", min=0, max=3)
    feature_bonus: int = factory.Faker("random_int", min=0, max=3)
    rerolls_ones: bool = factory.Faker("boolean")
    range: int = factory.Faker("random_int", min=5, max=300)
    attack_id: int


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
    hit_dice: str = factory.Faker("numerify", text="d#")
    proficiency: int = factory.Faker("random_int", min=1, max=5)
    armour_class: int = factory.Faker("random_int", min=1, max=20)
    weapon_proficiencies: list[enums.DndWeapons] = factory.LazyFunction(
        lambda: random.sample([x.value for x in enums.DndWeapons], random.randint(1, 3))
    )
    saving_throw_proficiencies: list[enums.DndAbilities] = factory.LazyFunction(
        lambda: random.sample(
            [x.value for x in enums.DndAbilities], random.randint(2, 6)
        )
    )
    skill_proficiencies: list[enums.DndSkills] = factory.LazyFunction(
        lambda: random.sample([x.value for x in enums.DndSkills], random.randint(4, 7))
    )
    tool_proficiencies: list[enums.DndTools] = factory.LazyFunction(
        lambda: random.sample([x.value for x in enums.DndTools], random.randint(4, 7))
    )
    # attacks: list["DndAttack"]

    @factory.post_generation
    def generate_related_data(self: DndCharacter, create, extracted):
        if not create:
            return
        self.skill_expertises = random.sample(
            self.skill_proficiencies, random.randint(0, 3)
        )
        self.tool_expertises = random.sample(
            self.tool_proficiencies, random.randint(0, 3)
        )
        attack: DndAttack = DndAttackFactory(character_id=self.id)
        DndDamageFactory(attack_id=attack.id)
