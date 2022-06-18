from dataclasses import dataclass
from position import Position


class Move:
    """A class for representing a single move as a pair of positions.
    Tracks whether a move is an en passant capture or a castle for the rare cases that matters"""
    begin: Position
    target: Position
    is_ep_cap: bool
    is_castle: bool

    def __init__(self, begin, target, is_ep_cap=False, is_castle=False):
        self.begin = begin
        self.target = target
        self.is_ep_cap = is_ep_cap
        self.is_castle = is_castle

    def __eq__(self, __o):
        return self.begin == __o.begin and self.target == __o.target

    def __str__(self):
        return f'{self.begin} -> {self.target}'

    def __repr__(self):
        return self.__str__()
