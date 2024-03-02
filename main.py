from Aigent import AiAigent
from BayesNetwork import BayesNetwork
from Graph import Graph
from Parser import Parser
from GameMaster import GameMaster
from name_tuppels import Point





def main():
    parser = Parser()
    bayes_network = BayesNetwork(parser.blocks, parser.fragile, parser.v_packages, parser.season, parser.leakage)
    bayes_network.build_network()


def menu(network: BayesNetwork):
    str_menu = """
    Enter your choice:
    1. Reset evidence list to empty.
    2. Add piece of evidence to evidence list.
    3. Do probabilistic reasoning.
    4. Quit.
    """
    while True:
        print(str_menu)
        choice = input(str_menu)
        choice = int(choice)
        if choice == 1:
            network.reset_evidence()
        elif choice == 2:
            pass
        elif choice == 3:
            pass
        elif choice == 4:
            break



if __name__ == '__main__':
    main()
