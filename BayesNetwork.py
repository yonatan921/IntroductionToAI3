from BayesNode import SeasonNode, PackageNode, EdgeNode, BlockNode
from name_tuppels import SeasonMode


class BayesNetwork:
    def __init__(self, blocks, fragiles, packages, season, leak):
        self.blocks = blocks
        self.fragiles = fragiles
        self.packages = packages
        self.season = season
        self.leak = leak

    def build_network(self):
        self.season_node = self.build_season()
        self.pacakge_nodes = self.build_package(self.season_node)
        self.edge_nodes = self.build_edges(self.pacakge_nodes)

    def build_season(self):
        return SeasonNode(self.season)

    def build_package(self, season_node: SeasonNode) -> {PackageNode}:
        pacakge_nodes = set()
        for pacakge in self.packages:
            pacakge_nodes.add(PackageNode((season_node,), pacakge.prob, pacakge.point))
        # return {PackageNode((season_node,), pacakge.prob, pacakge.point) for pacakge in self.packages}
        return pacakge_nodes

    def build_edges(self, pacakge_nodes: {PackageNode}):
        edge_nodes = set()
        for edge in self.fragiles:
            parents: {PackageNode} = set()
            for pacakge_node in pacakge_nodes:
                if pacakge_node.point in [edge.v1, edge.v2]:
                    parents.add(pacakge_node)
            edge_nodes.add(EdgeNode(tuple(parents), prob=edge.prob, v1=edge.v1, v2=edge.v2, leakage=self.leak))

        for edge in self.blocks:
            parents: {PackageNode} = set()
            for pacakge_node in pacakge_nodes:
                if pacakge_node.point in [edge.v1, edge.v2]:
                    parents.add(pacakge_node)
            edge_nodes.add(BlockNode(tuple(parents), v1=edge.v1, v2=edge.v2))
        return edge_nodes

    def __str__(self):

        season = str(self.season_node)
        vertexs = ""
        for vertex in self.pacakge_nodes:
            vertexs += str(vertex)
        edges = ""
        for egde in self.edge_nodes:
            edges += str(egde)

        return season + vertexs + edges
