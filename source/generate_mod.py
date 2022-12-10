from enum import Enum


class GenerateModType(Enum):
    Base = 0  # at the beginning, cells of this type are placed, necessarily adjacent to each other
    Probability = 1  # randomly scattered on the Base blocks
    Count = 2  # installed randomly no more than a certain amount


class GenerateMod:
    def __init__(self, type: GenerateModType, value: float):
        self._type = type
        self._value = value

    @property
    def type(self):
        return self._type

    @property
    def value(self):
        return self._value
