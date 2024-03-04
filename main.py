from Aigent import AiAigent
from BayesNetwork import BayesNetwork
from BayesNode import SeasonNode, PackageNode
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
            prob_menu = """
Choose probabilistic reasoning:
1. What is the probability that each of the vertices contains packages?
2. What is the probability that each of the edges is blocked?
3. What is the distribution of the season variable?
4. Quit.
"""
            prob_choice = input(prob_menu)
            prob_choice = int(prob_choice)
            if prob_choice == 1:
                for vertex in network.pacakge_nodes:
                    vector = network.\
                        enumerate_ask_package(PackageNode(None,
                                                          [1, 0, 0],
                                                          vertex._id))

            elif prob_choice == 2:
                pass
            elif prob_choice == 3:
                vector = network.enumerate_ask_season(SeasonNode((1, 0, 0)))
                print(f"low season = {vector[0]}, medium season = {vector[1]}, high season = {vector[2]}")
            elif prob_choice == 4:
                break
        elif choice == 4:
            break


if __name__ == '__main__':
    main()
