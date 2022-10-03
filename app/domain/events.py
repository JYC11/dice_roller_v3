from typing import Optional

from dataclasses import dataclass


class Event:
    pass


@dataclass
class DiceRolled(Event):
    roll_number: int
    dice_result: int
    dice_results: list[int]
    modifier: int
    total: int
    dropped_roll: Optional[int]
