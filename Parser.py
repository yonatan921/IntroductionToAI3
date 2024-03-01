from typing import Tuple

from Aigent import StupidAigent, HumanAigent, InterferingAigent

import argparse

from Tile import Package
from name_tuppels import Point, VPackage, Edge


class Parser:

    def __init__(self):

        parser = argparse.ArgumentParser(description="Your program description here")
        # Adding the 'filename' and 'algo' arguments
        parser.add_argument('--file', dest='filename', help="Input file path for the program")

        # Parse the command-line arguments
        args = parser.parse_args()

        # Access the values using args.filename and args.algo
        filename = args.filename

        self.max_x = None
        self.max_y = None
        self.v_packages: {VPackage} = set()
        self.blocks: {Edge} = set()
        self.fragile: {Edge} = set()
        self.leakage: float = 0
        self.season: Tuple[float, float, float] = (0, 0, 0)
        with open(filename, "r") as file:
            lines = file.readlines()

        for line in lines:
            words = line.split()
            if  words  and  words[0][0] == "#":
                if self.command_word(words) == "X":
                    self.max_x = self.parse_x(words)
                elif self.command_word(words) == "Y":
                    self.max_y = self.parse_y(words)
                elif self.command_word(words) == "V":
                    self.v_packages.add(self.parse_vpackage(words))
                elif self.command_word(words) == "B":
                    self.blocks.add(self.parse_blocks(words))
                elif self.command_word(words) == "F":
                    self.fragile.add(self.parse_fragile(words))
                elif self.command_word(words) == "L":
                    self.leakage = self.parse_leakage(words)
                elif self.command_word(words) == "S":
                    self.season = self.parse_season(words)
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

    def parse_vpackage(self, words: [str]) -> VPackage:
        point = Point(int(words[1]), int(words[2]))
        f = words[3]
        prob = words[4]
        return VPackage(point, f, prob)

    def parse_blocks(self, words: [str]) -> Edge:
        org_point = Point(int(words[1]), int(words[2]))
        dst_point = Point(int(words[3]), int(words[4]))
        return Edge(org_point, dst_point, 1)

    def parse_fragile(self, words: [str]) -> Edge:
        org_point = Point(int(words[1]), int(words[2]))
        dst_point = Point(int(words[3]), int(words[4]))
        prob = float(words[5])
        return Edge(org_point, dst_point, prob)

    def parse_leakage(self, words: [str]):
        return float(words[1])

    def parse_season(self, words: [str]):
        return float(words[1]), float(words[2]), float(words[3])
