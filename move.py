from dataclasses import dataclass
from position import Position


@dataclass
class Move:
    """A class for representing a single move as a pair of positions"""
    begin: Position
    target: Position
    is_ep_cap: bool = False

    def __eq__(self, __o):
        return self.begin == __o.begin and self.target == __o.target

    def __str__(self):
        return f'{self.begin} -> {self.target}'

    def __repr__(self):
        return self.__str__()
