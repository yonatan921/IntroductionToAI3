from typing import Tuple

from name_tuppels import Point, SeasonMode


class BayesNode:
    def __init__(self, parents, prob_table: {Tuple: float} = None, _id=0):
        self._id = _id
        self.parents = parents
        self.prob_table = prob_table


class SeasonNode(BayesNode):
    _id_counter = 0

    def __init__(self, prob: Tuple[float, float, float] = None):
        super().__init__(None, {(True, False, False): prob[0],
                                (False, True, False): prob[1],
                                (False, False, True): prob[2]}, SeasonNode._id_counter)
        SeasonNode._id_counter += 1

    def __str__(self):
        return f"""
SEASON:
    P(low) = {self.prob_table[(SeasonMode.LOW,)]}
    P(medium) = {self.prob_table[(SeasonMode.MEDIUM,)]}
    P(high) = {self.prob_table[(SeasonMode.HIGH,)]}
    
"""


class PackageNode(BayesNode):
    def __init__(self, parents: Tuple[SeasonNode], prob: float = None, package_point: Point = None):
        super().__init__(parents, {(True, False, False): min(1, prob),
                                   (False, True, False): min(1, 2 * prob),
                                   (False, False, True): min(1, 3 * prob)
                                   }, package_point)

    def __str__(self):
        return f"""
VERTEX ({self._id.x}, {self._id.y})
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
                                   (True, True): 1 - (1 - prob) ** 2 if len(parents) > 1 else 0}, (v1, v2))

    def __str__(self):
        return f"""
EDGE ({self._id[0].x}, {self._id[0].y}) ({self._id[1].x}, {self._id[1].y})
    P(blocked| no package ({self._id[0].x}, {self._id[0].y}), no package ({self._id[1].x}, {self._id[1].y}) = {self.prob_table[(False, False)]}
    P(blocked| no package ({self._id[0].x}, {self._id[0].y}), package ({self._id[1].x}, {self._id[1].y}) = {self.prob_table[(False, True)]}
    P(blocked| package ({self._id[0].x}, {self._id[0].y}), no package ({self._id[1].x}, {self._id[1].y}) = {self.prob_table[(True, False)]}
    P(blocked| package ({self._id[0].x}, {self._id[0].y}), package ({self._id[1].x}, {self._id[1].y}) = {self.prob_table[(True, True)]}
    
"""


class BlockNode(BayesNode):
    def __init__(self, parents: Tuple[PackageNode], v1: Point = None, v2: Point = None):
        super().__init__(parents, {(False, False): 1,
                                   (False, True): 1,
                                   (True, False): 1,
                                   (True, True): 1}, (v1, v2))

    def __str__(self):
        return f"""
EDGE ({self._id[0].x}, {self._id[0].y}) ({self._id[1].x}, {self._id[1].y})
    P(blocked| no package ({self._id[0].x}, {self._id[0].y}), no package ({self._id[1].x}, {self._id[1].y}) = {self.prob_table[(False, False)]}
    P(blocked| no package ({self._id[0].x}, {self._id[0].y}), package ({self._id[1].x}, {self._id[1].y}) = {self.prob_table[(False, True)]}
    P(blocked| package ({self._id[0].x}, {self._id[0].y}), no package ({self._id[1].x}, {self._id[1].y}) = {self.prob_table[(True, False)]}
    P(blocked| package ({self._id[0].x}, {self._id[0].y}), package ({self._id[1].x}, {self._id[1].y}) = {self.prob_table[(True, True)]}

"""
