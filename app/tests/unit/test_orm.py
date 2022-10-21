from sqlalchemy.orm import Session

from app.domain import models


def test_mappers(db: Session):
    assert True


def test_dnd_character_can_load_lines(db: Session):
    db.execute(
        "INSERT INTO dnd_characters (name, level, hp, race, background, class_info, strength, dexterity, constitution, intelligence, wisdom, charisma, hit_dice, proficiency, armour_class) VALUES"
        '("Rich", 12, 98, "Human", "Urban Bounty Hunter", "Warlock-Hexblade-11/Sorcerer-Shadow-1", 10, 14, 16, 11, 10, 20, "11d8,1d6", 4, 14),'
        '("Gronk", 3, 17, "Gnome, Rock", "Clan Crafter", "Artificer-Alchemist-3", 8, 15, 15, 16, 12, 8, "3d8", 2, 17),'
        '("Francois", 10, 103, "Dwarf, Hill", "Far Traveller", "Cleric-Tempest-10", 7, 16, 18, 14, 20, 13, "10d8", 4, 14)'
    )
    all = db.query(models.DndCharacter).all()
    assert all
