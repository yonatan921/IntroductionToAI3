from Aigent import StupidAigent, HumanAigent, InterferingAigent

import argparse

from Tile import Package
from name_tuppels import Point


class Parser:

    def __init__(self):
        strategy = {
            "cooperative": lambda p1, p2: p1 + p2,
            "semi": lambda p1, p2: p1,
            "adversarial": lambda p1, p2: p1 - p2
        }
        parser = argparse.ArgumentParser(description="Your program description here")
        # Adding the 'filename' and 'algo' arguments
        parser.add_argument('--file', dest='filename', help="Input file path for the program")
        parser.add_argument('--utility', help="Strategy for mini max algorithm: cooperative, semi, adversarial ")

        # Parse the command-line arguments
        args = parser.parse_args()

        # Access the values using args.filename and args.algo
        filename = args.filename

        if args.utility == "cooperative":
            print("Mode: cooperative TS1 = TS2 = IS1 + IS2")
        elif args.utility == "semi":
            print("Mode: semi TS1 = IS1, TS2 = IS2")
        elif args.utility == "adversarial":
            print("Mode: adversarial TS1 = IS1 - IS2, TS2 = IS2 - IS1")
        else:
            raise Exception
        self.utility = strategy[args.utility]

        self.max_x = None
        self.max_y = None
        self.packages: {Package} = set()
        self.blocks: {frozenset} = set()
        self.fragile: {frozenset} = set()
        self.agents = []
        with open(filename, "r") as file:
            lines = file.readlines()

        for line in lines:
            words = line.split()
            if words:
                if self.command_word(words) == "X":
                    self.max_x = self.parse_x(words)
                elif self.command_word(words) == "Y":
                    self.max_y = self.parse_y(words)
                elif self.command_word(words) == "P":
                    self.packages.add(self.parse_package(words))
                elif self.command_word(words) == "B":
                    self.blocks.add(self.parse_blocks(words))
                elif self.command_word(words) == "F":
                    self.fragile.add(self.parse_fragile(words))
                # elif self.command_word(words) == "A":
                #     self.agents.append(StupidAigent(self.parse_greedy_aigent(words)))
                # elif self.command_word(words) == "H":
                #     self.agents.append(HumanAigent(self.parse_human_aigent(words)))
                # elif self.command_word(words) == "I":
                #     self.agents.append(InterferingAigent(self.parse_interfering_aigent(words)))

    def command_word(self, words: [str]) -> str:
        return words[0][1]

    def parse_x(self, words: [str]) -> int:
        return int(words[1])

    def parse_y(self, words: [str]) -> int:
        return int(words[1])

    def parse_package(self, words: [str]) -> Package:
        org_point = Point(int(words[1]), int(words[2]))
        from_time = int(words[3])
        dst_point = Point(int(words[5]), int(words[6]))
        dead_line = int(words[7])
        return Package(org_point, from_time, dst_point, dead_line)

    def parse_blocks(self, words: [str]) -> frozenset:
        org_point = Point(int(words[1]), int(words[2]))
        dst_point = Point(int(words[3]), int(words[4]))
        return frozenset({org_point, dst_point})

    def parse_fragile(self, words: [str]) -> frozenset:
        org_point = Point(int(words[1]), int(words[2]))
        dst_point = Point(int(words[3]), int(words[4]))
        return frozenset({org_point, dst_point})

    def parse_greedy_aigent(self, words: [str]) -> Point:
        return Point(int(words[1]), int(words[2]))

    def parse_human_aigent(self, words: [str]) -> Point:
        return Point(int(words[1]), int(words[2]))

    def parse_interfering_aigent(self, words: [str]) -> Point:
        return Point(int(words[1]), int(words[2]))
