from dataclasses import dataclass
from position import Position


@dataclass
class Move:
    """A class for representing a single move as a pair of positions"""
    begin: Position
    target: Position

    def __str__(self):
        return f'{self.begin} -> {self.target}'