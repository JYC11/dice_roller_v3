from typing import Optional
from dataclasses import dataclass

from app.enums import enums


class Command:
    pass


@dataclass
class RollDice(Command):
    game_type: enums.GameType
    prefix: str
    multiplier: int
    dice_count: int
    dice_size: int
    modifier: int
    threshold: Optional[int] = None
    crit_threshold: Optional[int] = 20


@dataclass
class MetaCommand(Command):
    meta_command: str
