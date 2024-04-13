# Introduction to Artificial Intelligence - Programming Assignment 3

## Reasoning under Uncertainty - MAPD Problem: Locate the Blockages and Packages

This repository contains the solution to Programming Assignment 3, focusing on probabilistic reasoning using Bayes networks to address uncertainty.

### Goals
The primary goal of this assignment is to implement probabilistic reasoning techniques to reason about the uncertain environment of the MAPD problem, specifically focusing on locating blockages and packages.

### Uncertain MAPD Problem - Domain Description
In real-world scenarios, robots navigating through environments may encounter uncertainties such as unknown package locations and blocked edges. The goal is to plan optimal paths considering these uncertainties. The problem involves probabilistic reasoning using Bayes networks, where evidence (observations) is used to infer the likely locations of blockages, packages, and the current season (demand level).

### Solution Method
The solution method involves constructing a Bayes network according to the scenario described. The network comprises nodes representing blockages, package presence, and season, with conditional probability distributions specified based on known distributions and evidence provided. Probabilistic reasoning algorithms such as variable elimination or sampling are used to perform inference and answer queries about the distributions of blockages, package presence, and season.

### Requirements
1. **Part I**:
   - Read data, including distribution parameters, and construct the Bayes network.
   - Output the constructed Bayes network along with conditional probability distributions.
2. **Part II**:
   - Support interactive operations:
     - Reset evidence list.
     - Add evidence to the evidence list.
     - Perform probabilistic reasoning and report results.
     - Quit.

### Deliverables
- Source code 
- Explanation of the method for constructing the Bayes network and reasoning algorithm: _Below_
- Non-trivial example runs on at least 2 scenarios, including input and output


### How to Run
- To run the program, ensure you have Python 3 installed. Then execute the following command:
- python3 main.py --file <input_file_path>

- Replace <input_file_path> with the path to your input file containing graph information.
The program will read this file, compute the optimal policy using the described approach,
and provide output accordingly.

### Explanation 

#### Constructing the Bayes Network
The Bayes network is constructed in a way that captures the dependencies between the variables in the MAPD problem domain. Specifically, the network is structured such that:

1. **Season (Seacon)**:
   - The season variable represents the demand level in the environment, categorized into low, medium, and high. It serves as the root node of the Bayes network, influencing the likelihood of package presence and edge blockages.

2. **Package Presence**:
   - The package presence variable is conditioned on the season variable. The presence of packages at each vertex is influenced by the demand level of the season. For example, during periods of high demand, the likelihood of packages being present at vertices increases.

3. **Edge Blockages**:
   - The edge blockage variables are conditioned on both the package presence and the season variables. The likelihood of edges being blocked is influenced by the presence of packages at adjacent vertices and the demand level of the season. For instance, edges near vertices with packages are more likely to be blocked.

By structuring the Bayes network in this manner, with season influencing package presence, which in turn influences edge blockages, we can effectively model the uncertainties present in the MAPD problem environment. This allows us to perform probabilistic reasoning to infer the likely distributions of blockages, package presence, and season given observed evidence.

#### Probabilistic Reasoning
To perform inference on the constructed Bayes network and infer the likely distributions of variables given observed evidence, the `enumerate_all` algorithm is employed. This algorithm systematically enumerates all possible combinations of variable assignments, calculating the joint probability distribution over all variables in the network. By enumerating all possible assignments and summing their probabilities, we can obtain the marginal probabilities of interest, such as the probability of blockages, package presence, and season given the observed evidence.

Using the `enumerate_all` algorithm for probabilistic reasoning allows us to efficiently compute posterior probabilities and answer queries about the distributions of variables in the MAPD problem domain.