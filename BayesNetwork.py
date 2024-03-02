import copy

from BayesNode import SeasonNode, PackageNode, EdgeNode, BlockNode, BayesNode
from name_tuppels import SeasonMode


class BayesNetwork:
    def __init__(self, blocks, fragiles, packages, season, leak):
        self.blocks = blocks
        self.fragiles = fragiles
        self.packages = packages
        self.season = season
        self.leak = leak
        self.evidence: [{BayesNode: float}] = []

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
        # return {PackageNode((season_node,), pacakge.prob, pacakge.point) for pacakge in self.packages}
        return pacakge_nodes

    def build_edges(self, pacakge_nodes: {PackageNode}):
        edge_nodes = []
        for edge in self.fragiles:
            parents: {PackageNode} = set()
            for pacakge_node in pacakge_nodes:
                if pacakge_node.point in [edge.v1, edge.v2]:
                    parents.add(pacakge_node)
            edge_nodes.append(EdgeNode(tuple(parents), prob=edge.prob, v1=edge.v1, v2=edge.v2, leakage=self.leak))

        for edge in self.blocks:
            parents: {PackageNode} = set()
            for pacakge_node in pacakge_nodes:
                if pacakge_node.point in [edge.v1, edge.v2]:
                    parents.add(pacakge_node)
            edge_nodes.add(BlockNode(tuple(parents), v1=edge.v1, v2=edge.v2))
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
        Y = variables[0]
        if Y in evidence:
            value = evidence[Y]
            return y.prob_table

    def enumerate_ask_season(self, season: SeasonNode):
        q_x = [None, None, None]
        for value in season.prob_table:
            new_evidence = copy.deepcopy(self.evidence)
            new_evidence.append(value)
            variables = [self.season_node] + self.pacakge_nodes + self.edge_nodes
            q_x = enumerate_all(variables, new_evidence)

    def __str__(self):

        season = str(self.season_node)
        vertexs = ""
        for vertex in self.pacakge_nodes:
            vertexs += str(vertex)
        edges = ""
        for egde in self.edge_nodes:
            edges += str(egde)

        return season + vertexs + edges
