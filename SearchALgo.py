import abc
import heapq
from typing import Callable, Optional, Any, Tuple

from Graph import Graph
from Node import Node
from Problem import Problem
from ReturnStatus import ReturnStatus


class SearchALgo(abc.ABC):
    def __init__(self):
        self.expands_nums = 0

    def run_algo(self, problem: Problem, heuristic: Callable[[Graph], int]) -> Tuple[Optional[Node], ReturnStatus]:
        heap: [Node] = []
        init_node = Node(None, problem.init_state.agents[0].point, problem.init_state, 0, 0, heuristic, self.evaluation)
        heapq.heappush(heap, init_node)
        closed: {Node: int} = {}
        while heap:
            node = heapq.heappop(heap)
            self.expands_nums += 1
            if problem.goal_state(node.state):
                return node, ReturnStatus.Good
            if self.check_expansion_limit():
                return self.handle_expansion_limit(node)
            if node not in closed or node.evaluation < closed[node]:
                closed[node] = node.evaluation
            successors = self.expand(node)
            for successor in successors:
                if successor not in closed:
                    heapq.heappush(heap, successor)

        return None, ReturnStatus.Fail

    def expand(self, node: Node) -> {Node}:
        successors = set()
        for action, result in node.find_successors().items():
            successor = Node(parent=node, action=action, state=result, depth=node.depth + 1,
                             path_cost=node.path_cost + node.state.edge_cost(node.action, action),
                             heuristic=node.heuristic, evaluation_func=self.evaluation)
            successors.add(successor)
        return successors

    @abc.abstractmethod
    def evaluation(self, node: Node, heuristic: Callable[[Graph], int]) -> int:
        pass

    @abc.abstractmethod
    def check_expansion_limit(self) -> bool:
        pass

    @abc.abstractmethod
    def handle_expansion_limit(self, node):
        pass


class GreedySearch(SearchALgo):
    def evaluation(self, node: Node, heuristic: Callable[[Graph], int]) -> int:
        return heuristic(node.state)

    def check_expansion_limit(self) -> bool:
        return False

    def handle_expansion_limit(self, node):
        pass


class AStar(SearchALgo):
    def __init__(self, expansion_limit=10_000):
        super().__init__()
        self.expansion_limit = expansion_limit

    def evaluation(self, node: Node, heuristic: Callable[[Graph], int]) -> int:
        return node.path_cost + heuristic(node.state)

    def check_expansion_limit(self) -> bool:
        return self.expands_nums >= self.expansion_limit

    def handle_expansion_limit(self, node):
        return node, ReturnStatus.Fail


class RealTimeAStar(AStar):
    def __init__(self, expansion_limit=10):
        super().__init__(expansion_limit)
        self.expansion_limit = expansion_limit

    def handle_expansion_limit(self, node):
        return node, ReturnStatus.Cutoff

