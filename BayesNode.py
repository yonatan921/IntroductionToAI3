from enum import Enum
from typing import Tuple

from name_tuppels import Point


class BayesNode:
    def __init__(self, parents, prob_table: {Tuple: float} = None):
        self.parents = parents
        self.prob_table = prob_table


class SeasonNode(BayesNode):
    options = [0, 1, 2]

    def __init__(self, prob: Tuple[float, float, float] = None):
        super().__init__(None, {(): {0: prob[0], 1: prob[1], 2: prob[2]}})
        self._id = 0

    def __eq__(self, other):
        return isinstance(other, SeasonNode)

    def __hash__(self):
        return hash(SeasonNode.__name__)

    def __str__(self):
        return f"""
SEASON:
    P(low) = {self.prob_table[()][0]}
    P(medium) = {self.prob_table[()][1]}
    P(high) = {self.prob_table[()][2]}
    
"""


class PackageNode(BayesNode):
    options = [True, False]

    def __init__(self, parents: Tuple[SeasonNode], prob: float = None, package_point: Point = None):
        super().__init__(parents, {(0,): {True: min(1, prob), False: 1 - min(1, prob)},
                                   (1,): {True: min(1, 2 * prob), False: 1 - min(1, 2 * prob)},
                                   (2,): {True: min(1, 3 * prob), False: 1 - min(1, 3 * prob)}
                                   })
        self._id = package_point

    def __eq__(self, other):
        return other._id == self._id

    def __hash__(self):
        return hash(self._id)

    def __str__(self):
        return f"""
VERTEX ({self._id.x}, {self._id.y})
    P(package|low) = {self.prob_table[(0,)][True]}
    P(package|medium) = {self.prob_table[(1,)][True]}
    P(package|high) = {self.prob_table[(2,)][True]}
        
"""


class EdgeNode(BayesNode):
    options = [True, False]

    def __init__(self, parents: Tuple[PackageNode], prob: float = None, v1: Point = None, v2: Point = None,
                 leakage: float = 0):
        super().__init__(parents, {(False, False): {True: leakage, False: 1 - leakage},
                                   (False, True): {True: prob, False: 1 - prob},
                                   (True, False): {True: prob, False: 1 - prob},
                                   (True, True): {True: 1 - (1 - prob) ** 2, False: 1 - (1 - (1 - prob) ** 2)}
                                   })
        self._id = (v1, v2)

    def __eq__(self, other):
        return other._id == self._id

    def __hash__(self):
        return hash(self._id)

    def __str__(self):
        return f"""
EDGE ({self._id[0].x}, {self._id[0].y}) ({self._id[1].x}, {self._id[1].y})
    P(blocked| no package ({self._id[0].x}, {self._id[0].y}), no package ({self._id[1].x}, {self._id[1].y}) = {self.prob_table[(False, False)][True]}
    P(blocked| no package ({self._id[0].x}, {self._id[0].y}), package ({self._id[1].x}, {self._id[1].y}) = {self.prob_table[(False, True)][True]}
    P(blocked| package ({self._id[0].x}, {self._id[0].y}), no package ({self._id[1].x}, {self._id[1].y}) = {self.prob_table[(True, False)][True]}
    P(blocked| package ({self._id[0].x}, {self._id[0].y}), package ({self._id[1].x}, {self._id[1].y}) = {self.prob_table[(True, True)][True]}
    
"""


class BlockNode(BayesNode):
    options = [True, False]

    def __init__(self, parents: Tuple[PackageNode], v1: Point = None, v2: Point = None):
        super().__init__(parents, {(False, False): {True: 1, False: 0},
                                   (False, True): {True: 1, False: 0},
                                   (True, False): {True: 1, False: 0},
                                   (True, True): {True: 1, False: 0}})
        self._id = (v1, v2)

    def __eq__(self, other):
        return other._id == self._id

    def __hash__(self):
        return hash(self._id)

    def __str__(self):
        return f"""
EDGE ({self._id[0].x}, {self._id[0].y}) ({self._id[1].x}, {self._id[1].y})
    P(blocked| no package ({self._id[0].x}, {self._id[0].y}), no package ({self._id[1].x}, {self._id[1].y}) = {self.prob_table[(False, False)][True]}
    P(blocked| no package ({self._id[0].x}, {self._id[0].y}), package ({self._id[1].x}, {self._id[1].y}) = {self.prob_table[(False, True)][True]}
    P(blocked| package ({self._id[0].x}, {self._id[0].y}), no package ({self._id[1].x}, {self._id[1].y}) = {self.prob_table[(True, False)][True]}
    P(blocked| package ({self._id[0].x}, {self._id[0].y}), package ({self._id[1].x}, {self._id[1].y}) = {self.prob_table[(True, True)][True]}

"""
