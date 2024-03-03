import copy
from typing import Tuple, Any

from BayesNode import SeasonNode, PackageNode, EdgeNode, BlockNode, BayesNode
from name_tuppels import SeasonMode, Point


class BayesNetwork:
    def __init__(self, blocks, fragiles, packages, season, leak):
        self.blocks = blocks
        self.fragiles = fragiles
        self.packages = packages
        self.season = season
        self.leak = leak
        self.evidence: {Any: (Tuple[bool], bool)} = {}

    def build_network(self):
        self.season_node = self.build_season()
        self.pacakge_nodes = self.build_package(self.season_node)
        self.edge_nodes = self.build_edges(self.pacakge_nodes)

    def build_season(self):
        return SeasonNode(self.season)

    def build_package(self, season_node: SeasonNode) -> {PackageNode}:
        pacakge_nodes = []
        for pacakge in self.packages:
            pacakge_nodes.append(PackageNode((season_node,), pacakge.prob, pacakge.point))
        return pacakge_nodes

    def build_edges(self, pacakge_nodes: {PackageNode}):
        edge_nodes = []
        for edge in self.fragiles:
            parents: {PackageNode} = set()
            for pacakge_node in pacakge_nodes:
                if pacakge_node._id in [edge.v1, edge.v2]:
                    parents.add(pacakge_node)
            edge_nodes.append(EdgeNode(tuple(parents), prob=edge.prob, v1=edge.v1, v2=edge.v2, leakage=self.leak))

        for edge in self.blocks:
            parents: {PackageNode} = set()
            for pacakge_node in pacakge_nodes:
                if pacakge_node._id in [edge.v1, edge.v2]:
                    parents.add(pacakge_node)
            edge_nodes.append(BlockNode(tuple(parents), v1=edge.v1, v2=edge.v2))
        return edge_nodes

    def enumerate_ask(self, x_query):
        if isinstance(x_query, SeasonMode):
            self.enumerate_ask_season(x_query)
        else:
            q_x = [None, None]
        pass

    def enumerate_all(self, variables, evidence):
        if not variables:
            return 1
        bayes_node: BayesNode = variables[0]
        y = evidence.get(bayes_node._id)
        if y is not None:
            return bayes_node.prob_table[y[0]] * self.enumerate_all(variables[1:], evidence)
        if isinstance(bayes_node, EdgeNode) or isinstance(bayes_node, BlockNode):
            values = [(False, False), (False, True), (True, False), (True, True)]
        else:
            values = [(True, False, False), (False, True, False), (False, False, True)]
        probs = 0
        for value in values:
            evidence[bayes_node._id] = None
            evidence[bayes_node._id] = (bayes_node._id, True)
            probs += bayes_node.prob_table[value] * self.enumerate_all(variables[1:], evidence)
        return probs


    def enumerate_ask_season(self, season: Tuple[bool]):
        q_x = [{SeasonMode.LOW: None}, {SeasonMode.MEDIUM: None}, {SeasonMode.HIGH: None}]
        for index, season_mode in enumerate(season):
            new_evidence = copy.deepcopy(self.evidence)
            new_evidence[0] = (season, True)
            variables = [self.season_node] + self.pacakge_nodes + self.edge_nodes
            # q_x[index][season]] = self.enumerate_all(variables, new_evidence)
            a = self.enumerate_all(variables, new_evidence)

    def __str__(self):
        season = str(self.season_node)
        vertexs = ""
        for vertex in self.pacakge_nodes:
            vertexs += str(vertex)
        edges = ""
        for egde in self.edge_nodes:
            edges += str(egde)

        return season + vertexs + edges

    def reset_evidence(self):
        self.evidence = {}

    def add_evidence(self):
        str_menu = """
Enter your choice:
1. Add season
2. Add package
3. Add edge
4. Quit.
"""
        while True:
            choice = input(str_menu)
            choice = int(choice)
            if choice == 1:
                self.add_season()
            elif choice == 2:
                self.add_package()
            elif choice == 3:
                self.add_edge()
            elif choice == 4:
                break
            print(self.evidence)

    def add_season(self):
        str_menu = """
Enter season:
1. LOW
2. MEDIUM
3. HIGH
4. Quit.
"""
        while True:
            choice = input(str_menu)
            choice = int(choice)

            if choice == 1:
                self.remove_duplicate_evidance()
                self.evidence[0] = ((True, False, False), True)

            elif choice == 2:
                self.remove_duplicate_evidance()
                self.evidence[0] = ((False, True, False), True)

            elif choice == 3:
                self.remove_duplicate_evidance()
                self.evidence[0] = ((False, False, True), True)

            elif choice == 4:
                break

    def add_package(self):
        str_menu = """
Enter package location:
Enter x
"""

        x = input(str_menu)
        x = int(x)
        y = input("Enter y")
        y = int(y)
        p = Point(x, y)
        self.remove_duplicate_evidance(p)
        bool_pacakge = input("Enter True for exists package False else")
        bool_pacakge = bool_pacakge.lower() == "true"
        self.evidence[p] = {p: bool_pacakge}

    def add_edge(self):
        str_menu = """
Enter edge vertices:
Enter first vertex:
Enter X
"""
        x = input(str_menu)
        x_1 = int(x)
        y = input("Enter y")
        y_1 = int(y)
        x = input("Enter second vertex"
                  "Enter x")
        x_2 = int(x)
        y = input("Enter y")
        y_2 = int(y)
        p = (Point(x_1, y_1), Point(x_2, y_2))
        self.remove_duplicate_evidance(p)
        bool_blocked = input("Enter True for blocked edge False else")
        bool_blocked = bool_blocked.lower() == "true"
        self.evidence[p] = {p: bool_blocked}

    def remove_duplicate_evidance(self, key=None):
        if key in self.evidence:
            self.evidence.pop(key)
