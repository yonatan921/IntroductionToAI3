from typing import Tuple, Callable

from Graph import Graph
from Problem import Problem
from name_tuppels import Point


class MiniMax:

    def __init__(self, problem: Problem, cutoff_deep):
        self.problem = problem
        self.cutoff_deep = cutoff_deep

    def mini_max_decision(self, graph: Graph, aigent_id) -> Point:
        max_value, action, _, _ = self.max_value(graph, float("-inf"), float("inf"), 0, aigent_id, self.min_value)
        return action

    def maxi_max_decision(self, graph: Graph, aigent_id) -> Point:
        max_value, action = self.new_maxi_max(graph, 0, aigent_id)
        return action

    def max_value(self, caller_aigent, graph: Graph, a, b, deep, aigent_id, min_max: Callable) -> Tuple[
        int, Point, int, int]:
        aigent = graph.find_aigent_by_id(aigent_id)
        ts = (IS1, IS2) = graph.calc_heuristic(aigent_id)
        # TS1 = graph.utility(IS1, IS2)
        if graph.game_over() or deep == self.cutoff_deep:
            if deep == self.cutoff_deep:
                # print(f"MAX- {aigent_id=}, {IS1=}, {IS2=}, {TS1=}, {deep=}")

                pass
                # print(f"Cutoff!!! {aigent.point},{aigent_id} ")
            return ts[caller_aigent], aigent.point, IS1, IS2

        v = float("-inf")
        IS2_max = IS2
        best_action = None
        for action, state in self.problem.find_successors(graph).items():  # The smart aigent move
            x, min_action, new_IS1, new_IS2 = min_max(caller_aigent, state, float("-inf"), float("inf"), deep + 1,
                                                      1 - aigent_id, self.max_value)
            if x > v:
                v = x
                best_action = action
                IS2_max = new_IS2
            elif x == v:
                # new_p1, new_p2 = state.calc_heuristic(aigent_id)
                if new_IS2 > IS2_max:
                    IS2_max = new_IS2
                    v = x
                    best_action = action
            if v >= b:
                return v, action, IS1, IS2_max
            a = max(a, v)
        return v, best_action, IS1, IS2

    def min_value(self, graph: Graph, a, b, deep, aigent_id, min_max: Callable) -> Tuple[int, Point, int, int]:
        aigent = graph.find_aigent_by_id(aigent_id)
        IS1, IS2 = graph.calc_heuristic(aigent_id)
        TS2 = graph.utility(IS1, IS2)

        if graph.game_over() or deep == self.cutoff_deep:
            if deep == self.cutoff_deep:
                # print(f"MIN- {aigent_id=}, {IS1=}, {IS2=}, {TS2=}, {deep=}")
                pass
                # print(f"Cutoff!!! {aigent.point}")
            return TS2, aigent.point, IS1, IS2

        v = float("inf")
        IS2_max = IS2
        best_point = None
        for action, state in self.problem.find_successors(graph).items():  # The dummy aigent move
            x, max_action, new_IS1, newIS2 = min_max(state, a, b, deep + 1, 1 - aigent_id, self.min_value)
            if x < v:
                v = x
                best_point = max_action
                IS2_max = newIS2
            elif x == v:
                # new_p1, new_p2 = state.calc_heuristic(aigent_id)
                if newIS2 < IS2_max:
                    IS2_max = newIS2
                    v = x
                    best_point = action
            # v = min(v, self.max_value(state, a, b))
            if v <= a:
                return v, action, IS1, IS2_max
            b = min(b, v)
        return v, best_point, IS1, IS2_max

    def new_maxi_max(self, graph: Graph, deep, aigent_id) -> Tuple[int, Point]:
        aigent = graph.find_aigent_by_id(aigent_id)
        IS1, IS2 = graph.calc_heuristic(aigent_id)
        TS1 = graph.utility(IS1, IS2)
        TS2 = -1 * graph.utility(IS2, IS1)
        if graph.game_over() or deep == self.cutoff_deep:
            return TS1 if graph.turn % 2 == 0 else TS2, aigent.point

        best_h = float("-inf")
        best_move = None
        for action, state in self.problem.find_successors(graph).items():
            current_h, _ = self.new_maxi_max(state, deep + 1, aigent_id)
            if current_h > best_h:
                best_h = current_h
                best_move = action
        return best_h, best_move
