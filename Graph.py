from typing import Tuple

from Aigent import Aigent
from Tile import Tile, Package
from name_tuppels import Point


class Graph:
    def __init__(self, max_x: int, max_y: int, blocks: {frozenset}, fragile: {frozenset}, agents: [Aigent], timer,
                 packages, utility_func):
        self.grid = None
        self.edges = None
        self.relevant_packages = set()
        self.fragile = fragile
        self.agents: [Aigent] = agents
        self.init_grid(max_x, max_y, blocks)
        self.timer = timer
        self.all_packages = packages
        self.utility = utility_func
        self.turn = 0

    def init_grid(self, max_x, max_y, blocks: {frozenset}):
        self.grid = [[Tile(Point(i, j)) for i in range(max_x + 1)] for j in range(max_y + 1)]
        for aigent in self.agents:
            self.add_aigent(aigent)
        self.edges = self.create_neighbor_dict()
        for edge in blocks:
            self.remove_edge(edge)

    def game_over(self):
        return len(self.relevant_packages) == 0 and all([aigent.game_over() for aigent in self.agents])

    def add_aigent(self, aigent: Aigent):
        self.grid[aigent.point.y][aigent.point.x] = aigent

    def add_package(self, package: Package):
        for aigent in self.agents:
            if package.point == aigent.point:
                aigent.pakages.add(package)
                package.picked_up = True
                self.all_packages.remove(package)
                if package.point_dst == aigent.point:
                    aigent.pakages.remove(package)
                    aigent.score += 1
                return
        self.grid[package.point.y][package.point.x] = package

    def update_packages(self):
        self.relevant_packages = {package for package in self.all_packages if
                                  package.from_time <= self.timer <= package.dead_line and not package.picked_up}
        for package in self.relevant_packages:
            self.add_package(package)

        self.relevant_packages = {package for package in self.all_packages if
                                  package.from_time <= self.timer <= package.dead_line and not package.picked_up}

        # self.all_packages -= self.relevant_packages

    def can_move(self, location: Point, new_location: Point):
        if location == new_location:
            return True
        return self.edges[location].get(new_location) is not None and all(
            [aigent.point != new_location for aigent in self.agents])

    def get_packages_to_take(self):
        return {package.point for package in self.relevant_packages}

    def get_packages_to_deliver(self):
        return {package.point_dst for package in self.relevant_packages}

    def __str__(self):
        packegs_str = "Left packages " + str([package.to_string() for package in self.all_packages]) + "\n"
        aigents_string = str([aigent.string_state() for aigent in self.agents]) + "\n"
        matrix_string = "\n".join(" ".join(str(tile) for tile in row) for row in self.grid)
        return packegs_str + aigents_string + matrix_string + '\n'

    def remove_edge(self, edge: {Point}):
        p1, p2 = list(edge)
        if p1 in self.edges:
            del self.edges[p1][p2]
            del self.edges[p2][p1]

    def create_neighbor_dict(self):
        num_rows, num_cols = len(self.grid), len(self.grid[0])

        neighbor_dict = {
            Point(j, i): {
                Point(j, i - 1): 1 if i > 0 else None,
                Point(j, i + 1): 1 if i < num_rows - 1 else None,
                Point(j - 1, i): 1 if j > 0 else None,
                Point(j + 1, i): 1 if j < num_cols - 1 else None
            }
            for i in range(num_rows)
            for j in range(num_cols)
        }
        neighbor_dict = {coord: {k: v for k, v in neighbors.items() if v is not None} for coord, neighbors in
                         neighbor_dict.items()}

        return neighbor_dict

    def remove_fragile_edge(self, edge: {Point}):
        self.fragile.remove(edge)

    def remove_tile(self, point: Point):
        # remove agent
        self.grid[point.y][point.x] = Tile(point)

    def move_agent(self, org_point: Point, new_point: Point):
        # Add agent to new place
        get_agent = self.grid[org_point.y][org_point.x]
        self.grid[new_point.y][new_point.x] = get_agent

        # remove agent
        self.remove_tile(org_point)

    def available_moves(self, my_point: Point) -> [Point]:
        return [point for point, _ in self.edges[my_point].items() if
                point not in [aigent.point for aigent in self.agents]] + [my_point]

    def edge_cost(self, p1, p2) -> int:
        if p1 == p2:
            return 1
        dict1 = self.edges.get(p1)
        if not dict1:
            x = 6
        return dict1.get(p2)

    def __hash__(self):
        # Hash grid
        # hashable_attributes = [hash(tuple(map(hash, row))) for row in self.grid]

        # return hash(tuple(hashable_attributes))
        return hash(self.__key())

    def __eq__(self, other):
        if not isinstance(other, Graph):
            return False
        return self.__key() == other.__key()

    def calc_heuristic(self, aigent_id):
        p1 = self.agents[aigent_id].score + 0.5 * len(self.agents[aigent_id].pakages) + 0.25 * len(self.all_packages)
        p2 = self.agents[1 - aigent_id].score + 0.5 * len(self.agents[1 - aigent_id].pakages) + 0.25 * len(
            self.all_packages)
        return p1, p2

    def __key(self):
        return tuple(self.relevant_packages), tuple(self.fragile), tuple(self.agents)

    def find_aigent_by_id(self, _id):
        for aigent in self.agents:
            if aigent.id == _id:
                return aigent
