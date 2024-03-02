from Aigent import AiAigent
from BayesNetwork import BayesNetwork
from Graph import Graph
from Parser import Parser
from GameMaster import GameMaster
from name_tuppels import Point


def main():
    parser = Parser()
    bayesNetwork = BayesNetwork(parser.blocks, parser.fragile, parser.v_packages, parser.season, parser.leakage)
    bayesNetwork.build_network()
    print(bayesNetwork)
    # graph = Graph(parser.max_x, parser.max_y,  parser.blocks, parser.fragile, parser.agents, 0, parser.packages)
    # graph = Graph(parser.max_x, parser.max_y, parser.blocks, parser.fragile,
    #               [AiAigent(Point(0, 0), 0), AiAigent(Point(4, 0), 1)], 0,
    #               parser.packages, parser.utility)
    # game_master = GameMaster(graph, parser.packages)
    # game_master.start_game()


if __name__ == '__main__':
    main()
