import copy
from typing import Any

from BayesNode import SeasonNode, PackageNode, EdgeNode, BlockNode, BayesNode
from name_tuppels import Point


class BayesNetwork:
    def __init__(self, blocks, fragiles, packages, season, leak):
        self.blocks = blocks
        self.fragiles = fragiles
        self.packages = packages
        self.season = season
        self.leak = leak
        self.evidence: {BayesNode: Any} = {}

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

    def find_pacakge_node(self, p: Point) -> PackageNode:
        for pacakge_node in self.pacakge_nodes:
            if pacakge_node._id == p:
                return pacakge_node

    def find_edge_node(self, p1: Point, p2: Point) -> EdgeNode:
        for edge_node in self.edge_nodes:
            if edge_node._id == (p1, p2) or edge_node._id == (p2, p1):
                return edge_node

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

    def enumerate_all(self, variables: [BayesNode], evidence: {BayesNode: Any}):
        if not variables:
            return 1

        bayes_node = variables[0]

        # Check if the current BayesianNode is in the evidence
        for node in evidence:
            if bayes_node == node:
                # Calculate the conditional probability based on evidence
                parents_values = tuple(evidence[parent] for parent in node.parents) if node.parents else ()
                d = node.prob_table.get(parents_values, {})
                p = d.get((evidence[bayes_node])) if isinstance(evidence[bayes_node], int) else d.get(
                    tuple(evidence[bayes_node]))
                return p * self.enumerate_all(variables[1:], evidence)

        probs = 0
        dicts = [bayes_node.prob_table.get(parents_values, {}) for parents_values in bayes_node.prob_table.keys()]
        for option in bayes_node.options:
            new_evidance = copy.deepcopy(evidence)
            new_evidance[bayes_node] = option
            numerate_prob = self.enumerate_all(variables[1:], new_evidance)
            probs += sum(
                [d.get((tuple([new_evidance[bayes_node]])), d.get(new_evidance[bayes_node], )) * numerate_prob for
                 d in dicts])

        return probs

    def enumerate_ask_season(self):
        q_x = [0, 0, 0]
        node = self.season_node
        for evident, mode in self.evidence.items():
            if node == evident:
                q_x[mode] = 1
                return q_x

        for index, season_mode in enumerate([0, 1, 2]):
            new_evidence = copy.deepcopy(self.evidence)
            new_evidence[node] = season_mode
            variables = [self.season_node] + self.pacakge_nodes + self.edge_nodes
            q_x[index] = self.enumerate_all(variables, new_evidence)
        return self.normal_vector(q_x)

    def enumerate_ask_package(self, node: BayesNode):
        q_x = [0, 0]
        for evident, exist in self.evidence.items():
            if node == evident:
                q_x[0 if exist else 1] = 1
                return q_x

        for index, key in enumerate([True, False]):
            new_evidence = copy.deepcopy(self.evidence)
            new_evidence[node] = key
            variables = [self.season_node] + self.pacakge_nodes + self.edge_nodes
            q_x[index] = self.enumerate_all(variables, new_evidence)
        return self.normal_vector(q_x)

    def enumerate_ask_edge(self, node: BayesNode):
        if isinstance(node, BlockNode):
            return [1, 0]
        q_x = [0, 0]
        for evident, exist in self.evidence.items():
            if node == evident:
                q_x[0 if exist else 1] = 1
                return q_x

        for index, key in enumerate([True, False]):
            new_evidence = copy.deepcopy(self.evidence)
            new_evidence[node] = key
            variables = [self.season_node] + self.pacakge_nodes + self.edge_nodes
            q_x[index] = self.enumerate_all(variables, new_evidence)
        return self.normal_vector(q_x)

    def normal_vector(self, vector: [float]):
        num_sum = sum(vector)
        return [num / num_sum for num in vector]

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
                self.evidence[self.season_node] = 0
            elif choice == 2:
                self.evidence[self.season_node] = 1
            elif choice == 3:
                self.evidence[self.season_node] = 2
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
        bool_pacakge = input("Enter True for exists package False else")
        bool_pacakge = bool_pacakge.lower() == "true"
        package_node = self.find_pacakge_node(Point(x, y))
        self.evidence[package_node] = bool_pacakge

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
        x = input("Enter second vertex\nEnter x")
        x_2 = int(x)
        y = input("Enter y")
        y_2 = int(y)
        p1 = Point(x_1, y_1)
        p2 = Point(x_2, y_2)
        bool_blocked = input("Enter True for blocked edge False else")
        bool_blocked = bool_blocked.lower() == "true"
        edge_node = self.find_edge_node(p1, p2)
        self.evidence[edge_node] = bool_blocked



