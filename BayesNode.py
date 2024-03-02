from enum import Enum
from typing import Tuple

from name_tuppels import Point, SeasonMode


class BayesNode:
    def __init__(self, parents, prob_table: {Tuple: float} = None):
        self.parents = parents
        self.prob_table = prob_table


class SeasonNode(BayesNode):

    def __init__(self, prob: Tuple[float, float, float] = None):
        super().__init__(None, {(SeasonMode.LOW,): prob[0],
                                (SeasonMode.MEDIUM,): prob[1],
                                (SeasonMode.HIGH,): prob[2]})

    def __str__(self):
        return f"""
SEASON:
    P(low) = {self.prob_table[(SeasonMode.LOW,)]}
    P(medium) = {self.prob_table[(SeasonMode.MEDIUM,)]}
    P(high) = {self.prob_table[(SeasonMode.HIGH,)]}
    
                """


class PackageNode(BayesNode):
    def __init__(self, parents: Tuple[SeasonNode], prob: float = None, package_point: Point = None):
        super().__init__(parents, {(SeasonMode.LOW,): min(1, prob),
                                   (SeasonMode.MEDIUM,): min(1, 2 * prob),
                                   (SeasonMode.HIGH,): min(1, 3 * prob)
                                   })
        self.point = package_point

    def __str__(self):
        return f"""
VERTEX ({self.point.x}, {self.point.y})
    P(package|low) = {self.prob_table[(SeasonMode.LOW,)]}
    P(package|medium) = {self.prob_table[(SeasonMode.MEDIUM,)]}
    P(package|high) = {self.prob_table[(SeasonMode.HIGH,)]}
        
        """


class EdgeNode(BayesNode):
    def __init__(self, parents: Tuple[PackageNode], prob: float = None, v1: Point = None, v2: Point = None,
                 leakage: float = 0):
        super().__init__(parents, {(False, False): leakage,
                                   (False, True): prob if len(parents) > 1 else 0,
                                   (True, False): prob if len(parents) > 0 else 0,
                                   (True, True): 1 - (1 - prob) ** 2 if len(parents) > 1 else 0})

        self.points = (v1, v2)

    def __str__(self):
        return f"""
EDGE ({self.points[0].x}, {self.points[0].y}) ({self.points[1].x}, {self.points[1].y})
    P(blocked| no package ({self.points[0].x}, {self.points[0].y}), no package ({self.points[1].x}, {self.points[1].y}) = {self.prob_table[(False, False)]}
    P(blocked| no package ({self.points[0].x}, {self.points[0].y}), package ({self.points[1].x}, {self.points[1].y}) = {self.prob_table[(False, True)]}
    P(blocked| package ({self.points[0].x}, {self.points[0].y}), no package ({self.points[1].x}, {self.points[1].y}) = {self.prob_table[(True, False)]}
    P(blocked| package ({self.points[0].x}, {self.points[0].y}), package ({self.points[1].x}, {self.points[1].y}) = {self.prob_table[(True, True)]}
    
        """


class BlockNode(BayesNode):
    def __init__(self, parents: Tuple[PackageNode], v1: Point = None, v2: Point = None):
        super().__init__(parents, {(False, False): 1,
                                   (False, True): 1,
                                   (True, False): 1,
                                   (True, True): 1})

        self.points = (v1, v2)

    def __str__(self):
        return f"""
EDGE ({self.points[0].x}, {self.points[0].y}) ({self.points[1].x}, {self.points[1].y})
    P(blocked| no package ({self.points[0].x}, {self.points[0].y}), no package ({self.points[1].x}, {self.points[1].y}) = {self.prob_table[(False, False)]}
    P(blocked| no package ({self.points[0].x}, {self.points[0].y}), package ({self.points[1].x}, {self.points[1].y}) = {self.prob_table[(False, True)]}
    P(blocked| package ({self.points[0].x}, {self.points[0].y}), no package ({self.points[1].x}, {self.points[1].y}) = {self.prob_table[(True, False)]}
    P(blocked| package ({self.points[0].x}, {self.points[0].y}), package ({self.points[1].x}, {self.points[1].y}) = {self.prob_table[(True, True)]}

        """
