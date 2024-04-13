from collections import namedtuple
from enum import Enum

Point = namedtuple("Point", "x, y")
VPackage = namedtuple("VPackage", "point, f, prob")
Edge = namedtuple("Edge", "v1 ,v2,prob")


class SeasonMode(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3
