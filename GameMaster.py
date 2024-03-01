import copy

from Graph import Graph
from MiniMax import MiniMax
from Problem import Problem


class GameMaster:
    def __init__(self, graph: Graph, packages):
        self.graph = graph
        self.turn_index = 0
        self.all_packages = packages
        self.update_packages()
        self.graph.agents[0].problem = Problem(self.graph, lambda g: g.game_over())
        self.mini_max_algo = MiniMax(self.graph.agents[0].problem, cutoff_deep := 6)
        print(
            f"Heuristic is 1 point for delivered package 0.5 for carry package and 0.25 for unpicked package. {cutoff_deep=} ")

    def start_game(self):
        while not self.game_over():
            print(self)
            self.graph.timer += 1
            for aigent in self.graph.agents:
                self.update_packages()
                action = self.mini_max_algo.maxi_max_decision(self.graph, aigent.id)
                print(f"{action=}-------------")
                aigent.move_agent(self.graph, action)
                self.graph.turn += 1
        print(self)

    def game_over(self):
        return self.graph.game_over()

    def update_packages(self):
        self.update_graph_packages()
        self.update_aigent_packages()

    def update_aigent_packages(self):
        for aigent in self.graph.agents:
            aigent.update_packages(self.graph.timer)

    def update_graph_packages(self):
        self.graph.update_packages()

    def __str__(self):
        return str(self.graph)
