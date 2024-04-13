from BayesNetwork import BayesNetwork
from Parser import Parser


def main():
    parser = Parser()
    bayes_network = BayesNetwork(parser.blocks, parser.fragile, parser.v_packages, parser.season, parser.leakage)
    bayes_network.build_network()
    menu(bayes_network)


def menu(network: BayesNetwork):
    str_menu = """
Enter your choice:
0. Print network
1. Reset evidence list to empty.
2. Add piece of evidence to evidence list.
3. Do probabilistic reasoning.
4. Quit.
"""
    while True:
        choice = input(str_menu)
        if choice == "0":
            print(network)
        if choice == "1":
            network.reset_evidence()
        elif choice == "2":
            network.add_evidence()
        elif choice == "3":
            prob_menu = """
Choose probabilistic reasoning:
1. What is the probability that each of the vertices contains packages?
2. What is the probability that each of the edges is blocked?
3. What is the distribution of the season variable?
4. Quit.
"""
            while True:
                prob_choice = input(prob_menu)
                if prob_choice == "1":
                    print("The probability that each of the vertices contains packages is:")
                    for vertex in network.pacakge_nodes:
                        vector = network.\
                            enumerate_ask_package(vertex)
                        print(f"Vertex: {vertex._id}: {vector[0]}")

                elif prob_choice == "2":
                    print("The probability that each of the edges is blocked is:")
                    for edge in network.edge_nodes:
                        vector = network.enumerate_ask_edge(edge)
                        print(f"Edge: {edge._id}: {vector[0]}")

                elif prob_choice == "3":
                    print("The distribution of the season variable is:")
                    vector = network.enumerate_ask_season()
                    print(f"low season = {vector[0]}, medium season = {vector[1]}, high season = {vector[2]}")
                elif prob_choice == "4":
                    break
        elif choice == "4":
            break


if __name__ == '__main__':
    main()
