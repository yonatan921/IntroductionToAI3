from Aigent import AiAigent
from BayesNetwork import BayesNetwork
from BayesNode import PackageNode, SeasonNode
from Graph import Graph
from Parser import Parser
from GameMaster import GameMaster
from name_tuppels import Point


def main():
    parser = Parser()
    bayes_network = BayesNetwork(parser.blocks, parser.fragile, parser.v_packages, parser.season, parser.leakage)
    bayes_network.build_network()
    menu(bayes_network)


def menu(network: BayesNetwork):
    str_menu = """
Enter your choice:
1. Reset evidence list to empty.
2. Add piece of evidence to evidence list.
3. Do probabilistic reasoning.
4. Quit.
"""
    while True:
        choice = input(str_menu)
        choice = int(choice)
        if choice == 1:
            network.reset_evidence()
        elif choice == 2:
            network.add_evidence()
        elif choice == 3:
            x = network.enumerate_ask_season(SeasonNode((1, 0, 0)))
            print(x)
        elif choice == 4:
            break


if __name__ == '__main__':
    main()
