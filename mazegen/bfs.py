#!/usr/bin/env python3

from mazegen.maze_generator import Config
from mazegen.maze_gen_recursive import MazeGenerator
from collections import deque

class BreadthFirstSearch():
    def __init__(self, pos: list[list[int]], config: Config) -> None:
        self._pos = pos
        self._config = config

    def search_maze(self):
        start = tuple(self._config.ENTRY)
        goal = tuple(self._config.EXIT)

        queue = deque([start])
        visited = {start}
        parent = {start: None}

        while queue:
            x, y = queue.popleft()
            if (x, y) == goal:
                path = self.reconstruct_path(parent, goal)
                self._path = path
                path_cardinal = self.make_path_cardinal(path)
                self.show(path_cardinal)
                return
            cardinals = self.get_passible_cardinals(x, y)
            if not cardinals:
                continue
            for cardinal in cardinals:
                nx, ny = self.get_position_based_on_cardinal(x, y, cardinal)
                if (nx, ny) not in visited and self.is_road((x, y), (nx, ny)):
                    visited.add((nx, ny))
                    parent[(nx, ny)] = (x, y)
                    queue.append((nx, ny))
        return

    def get_passible_cardinals(self, x: int, y: int) -> None:
        cardinals = ["N", "E", "S", "W"]
        if y < 1:
            cardinals.remove("N")
        if x > self._config.WIDTH - 2:
            cardinals.remove("E")
        if y > self._config.HEIGHT - 2:
            cardinals.remove("S")
        if x < 1:
            cardinals.remove("W")
        return cardinals

    def get_position_based_on_cardinal(self, x:int, y:int, cardinal: str) -> tuple[int, int]:
        if cardinal == "N":
            return (x, y - 1)
        if cardinal == "E":
            return (x + 1, y)
        if cardinal == "S":
            return (x, y + 1)
        if cardinal == "W":
            return (x - 1, y)

    def reconstruct_path(self, parent: [tuple[int, int], tuple[int, int] | None], goal: tuple[int, int]) -> list[tuple[int, int]]:
        path = []
        node = goal
        while node is not None:
            path.append(node)
            node = parent[node]
        path.reverse()
        return path

    def make_path_cardinal(self, path: list[tuple[int, int]]) -> str:
        path_cardinal = []
        len_path = len(path)
        for i in range(len_path - 1):
            node1 = path[i]
            node2 = path[i + 1]
            x_1, y_1 = node1
            x_2, y_2 = node2
            if y_2 < y_1:
                path_cardinal.append("N")
            if x_2 > x_1:
                path_cardinal.append("E")
            if y_2 > y_1:
                path_cardinal.append("S")
            if x_2 < x_1:
                path_cardinal.append("W")
        return "".join(path_cardinal)

    def is_road(self, pos: tuple[int, int], n_pos: tuple[int, int]) -> bool:
        x, y = pos
        nx, ny = n_pos
        distance = (x - nx) ** 2 + (y - ny) ** 2
        if distance != 1:
            return False
        # ビット定義: N=8, E=4, S=2, W=1
        if ny < y and (self._pos[x][y].value & 8) == 0 and (self._pos[nx][ny].value & 2) == 0:
            return True
        if nx > x and (self._pos[x][y].value & 4) == 0 and (self._pos[nx][ny].value & 1) == 0:
            return True
        if ny > y and (self._pos[x][y].value & 2) == 0 and (self._pos[nx][ny].value & 8) == 0:
            return True
        if nx < x and (self._pos[x][y].value & 1) == 0 and (self._pos[nx][ny].value & 4) == 0:
            return True
        return False

    def show(self, path_cardinal: str) -> None:
        print(path_cardinal)


if __name__ == "__main__":
    maze = MazeGenerator()
    print("= 迷路生成前 =")
    maze.maze_show()
    print("= 迷路生成後（バックトラッキング） =")
    maze.maze_gen()
    maze.maze_show()
    print("= 最小経路探索（幅優先）=")
    bfs = BreadthFirstSearch(maze._pos, maze._config)
    bfs.search_maze()
