from maze_generator import Config, MazeGeneratorBasic
import numpy as np

class MazeGenerator(MazeGeneratorBasic):
    def maze_gen(self):
        """
        迷路の生成(recursive backtrack)


        """
        start_x = self._rng.integers(0, self._config.WIDTH)
        start_y = self._rng.integers(0, self._config.HEIGHT)
        start = (int(start_x), int(start_y))
        self._parent: dict[tuple[int, int], tuple[int, int] | None] = {start:None}
        self.change_to_visited(start)
        self.backtrack(start)

    def backtrack(self, start: tuple[int, int]) -> None:
        non_visited = self.get_non_visited_cardinal(start)
        x, y = start
        if self.check_all_visited():
            return
        if non_visited:
            cardinal = self._rng.choice(non_visited)
            self.break_wall(start, cardinal)
            self.append_parent(cardinal, start, self._parent)
            new_position = self.get_new_position(start, cardinal)
            self.change_to_visited(new_position)
        else:
            new_position = self.get_old_position(start, self._parent)
            self.pop_parent(start, self._parent)
        self.backtrack(new_position)

    def get_non_visited_cardinal(self, position: tuple[int, int]) -> list[str]:
        x, y = position
        non_visited = []
        if y > 0 and self._pos[x][y - 1].visited == False:
            non_visited.append("N")
        if x < self._config.WIDTH - 1 and self._pos[x + 1][y].visited == False:
            non_visited.append("E")
        if y < self._config.HEIGHT - 1 and self._pos[x][y + 1].visited == False:
            non_visited.append("S")
        if x > 0 and self._pos[x - 1][y].visited == False:
            non_visited.append("W")
        return non_visited

    def append_parent(self, cardinal: str, position: tuple[int, int], parent: dict[tuple[int, int], tuple[int, int] | None]) -> dict[tuple[int, int], tuple[int, int] | None]:
        x, y = position
        if cardinal == "N":
            parent[(x, y - 1)] = (x, y)
        if cardinal == "E":
            parent[(x + 1, y)] = (x, y)
        if cardinal == "S":
            parent[(x, y + 1)] = (x, y)
        if cardinal == "W":
            parent[(x - 1, y)] = (x, y)
        return parent

    def get_new_position(self, position: tuple[int, int], cardinal: str) -> tuple[int, int]:
        x, y = position
        if cardinal == "N":
            new_x = x
            new_y = y - 1
        if cardinal == "E":
            new_x = x + 1
            new_y = y
        if cardinal == "S":
            new_x = x
            new_y = y + 1
        if cardinal == "W":
            new_x = x - 1
            new_y = y
        return (new_x, new_y)

    def pop_parent(self, position: tuple[int, int], parent: dict[tuple[int, int], tuple[int, int] | None]) -> dict[tuple[int, int], tuple[int, int] | None]:
        x, y = position
        parent.pop((x, y))
        return parent

    def get_old_position(self, position: tuple[int, int], parent: dict[tuple[int, int], tuple[int, int] | None]) -> tuple[int, int]:
        old_position = parent[position]
        return old_position

    def check_all_visited(self) -> bool:
        result = True
        for x in range(self._config.WIDTH):
            for y in range(self._config.HEIGHT):
                result &= self._pos[x][y].visited
        return result


if __name__ == "__main__":
    maze = MazeGenerator()
    print("= 迷路生成前 =")
    maze.maze_show()
    print("= 迷路生成後 =")
    maze.maze_gen()
    maze.maze_show()
