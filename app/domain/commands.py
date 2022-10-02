from typing import Optional
from dataclasses import dataclass

from app.enums import enums


class Command:
    pass


@dataclass
class RollDice(Command):
    prefix: str
    multiplier: int
    dice_count: int
    dice_size: int
    modifier: int
    roll_type: Optional[enums.DndRollTypes] = None


@dataclass
class MetaCommand(Command):
    meta_command: str
