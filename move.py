from dataclasses import dataclass
from position import Position


@dataclass
class Move:
    """A class for representing a single move as a pair of positions"""
    begin: Position
    target: Position