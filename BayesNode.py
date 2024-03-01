from enum import Enum
from typing import Tuple

from name_tuppels import Point


class BayesNode:
    def __init__(self, parents, prob: float = None):
        self.prob = prob
        self.parents = parents
        self.prob_table: {Tuple: float} = {}


class SeasonNode(BayesNode):
    class SeasonMode(Enum):
        LOW = 1
        MEDIUM = 2
        HIGH = 3

    def __init__(self, prob: Tuple[float, float, float] = None):
        super().__init__(None, prob)


class PackageNode(BayesNode):
    def __init__(self, parents: Tuple[SeasonNode], prob: float = None, package_point: Point = None):
        super().__init__(parents, prob)
        self.point = package_point


class EdgeNode(BayesNode):
    def __init__(self, parents: Tuple[PackageNode], prob: float = None, v1: Point = None, v2: Point = None):
        super().__init__(parents, prob)
        self.points = {v1, v2}
