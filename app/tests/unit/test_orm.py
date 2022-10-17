from sqlalchemy.orm import Session

from app.domain import models


def test_mappers(session: Session):
    stuff = session.query(models.DndCharacter).all()
    assert True
