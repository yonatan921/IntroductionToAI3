# Project Assignment Three - Introduction to AI

## Reasoning under uncertaintyr using Python 3.8

### Overview

This project aims to solve probabilistic reasoning using Bayes networks, with scenarios similar to the MAPD problem, using various algorithms implemented in Python 3.8. 

### Getting Started

To run the program, follow the steps below:

1. Ensure you have Python 3.8 installed on your system.


## How to run
```bash
python3 main.py --file example.txt
```

When running the program you will see a menu with all the functions our program supports:

0. Print network
1. Reset evidence list to empty.
2. Add piece of evidence to evidence list.
3. Do probabilistic reasoning.
4. Quit.

Choose your option and continue as specified in the menu instructions

## Explanation of constructing the BN
Our BN is constructed with base node "Season Nodes", which are parents of "Package Nodes", which are parents of "Edge Nodes".
Each node has it's probability of having a specific value:
Season Node= "low", "medium" or "high", Package Node= contain package, and Edge Node= blocked.

We chose to implement the reasoning with "sampling enumeration" as studied in class.
## Running examples
Running examples in output_example_1,2.txt files