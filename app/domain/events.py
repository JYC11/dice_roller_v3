from typing import Optional

from dataclasses import dataclass

from app.enums import enums


class Event:
    pass


@dataclass
class DiceRolled(Event):
    game_type: enums.GameType
    roll_number: int
    dice_result: int
    dice_results: list[int]
    modifier: int
    total: int
    dropped_rolls: list[int]
    lower_rolls: list[int]
    critical: Optional[bool] = None
