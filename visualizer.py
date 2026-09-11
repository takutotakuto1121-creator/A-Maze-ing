from enum import Enum
from mazegen.maze_generator import Config, Cell
from mazegen.maze_gen_recursive import MazeGenerator
# from maze_gen_prims import MazeGeneratorPrims
# from maze_gen_kruskals import MazeGeneratorKruskals
from mazegen.bfs import BreadthFirstSearch
import os


class Color(Enum):
    WHITE = "\033[47m  \033[0m"
    BLACK = "\033[40m  \033[0m"
    BLUE = "\033[44m  \033[0m"
    RED = "\033[41m  \033[0m"
    GRAY = "\033[100m  \033[0m"
    GREEN = "\033[42m  \033[0m"          # 緑
    YELLOW = "\033[43m  \033[0m"         # 黄
    MAGENTA = "\033[45m  \033[0m"        # マゼンタ（紫）
    CYAN = "\033[46m  \033[0m"           # シアン（水色）
    BRIGHT_RED = "\033[101m  \033[0m"    # 明るい赤（朱色に近い）
    BRIGHT_GREEN = "\033[102m  \033[0m"  # 明るい緑（黄緑）
    BRIGHT_YELLOW = "\033[103m  \033[0m" # 明るい黄
    BRIGHT_MAGENTA = "\033[105m  \033[0m"# 明るいマゼンタ（ピンク）
    BRIGHT_CYAN = "\033[106m  \033[0m"   # 明るいシアン


class Visualizer():
    def __init__(self, pos: list[list[Cell]], config: Config, path) -> None:
        self._pos = pos
        self._config = config
        self._wall_color = Color.WHITE
        self._path = path
        self._show_path = False

    def visualize(self) -> None:
        self._visual = [
            [self._wall_color.value for _ in range(self._config.HEIGHT * 2 + 1)]
            for _ in range(self._config.WIDTH * 2 + 1)
        ]
        for x in range(self._config.WIDTH * 2 + 1):
            for y in range(self._config.HEIGHT * 2 + 1):
                if x % 2 == 1 and y % 2 == 1:
                    self.make_road(x, y)
        for x in range(self._config.WIDTH):
            for y in range(self._config.HEIGHT):
                self.make_wall(x, y)
        if self._show_path:
            self.make_shortest_path(self._path)
        for x in range(self._config.WIDTH):
            for y in range(self._config.HEIGHT):
                self.make_42_start_goal_min(x, y)

    def make_road(self, x:int, y:int) -> None:
        self._visual[x][y] = Color.BLACK.value

    def make_wall(self, x: int, y: int) -> None:
        if self._pos[x][y].value & 8 == 8:
            self._visual[x * 2 + 1][y * 2] = self._wall_color.value
        else:
            self._visual[x * 2 + 1][y * 2] = Color.BLACK.value
        if self._pos[x][y].value & 4 == 4:
            self._visual[x * 2 + 2][y * 2 + 1] = self._wall_color.value
        else:
            self._visual[x * 2 + 2][y * 2 + 1] = Color.BLACK.value
        if self._pos[x][y].value & 2 == 2:
            self._visual[x * 2 + 1][y * 2 + 2] = self._wall_color.value
        else:
            self._visual[x * 2 + 1][y * 2 + 2] = Color.BLACK.value
        if self._pos[x][y].value & 1 == 1:
            self._visual[x * 2][y * 2 + 1] = self._wall_color.value
        else:
            self._visual[x * 2][y * 2 + 1] = Color.BLACK.value

    def make_42_start_goal_min(self, x: int, y: int):
        if self._pos[x][y].is_42:
            self._visual[x * 2 + 1][y * 2 + 1] = Color.GRAY.value
        if self._pos[x][y].is_min:
            self._visual[x * 2 + 1][y * 2 + 1] = Color.BLUE.value
        if (x, y) == self._config.ENTRY or (x, y) == self._config.EXIT:
            self._visual[x * 2 + 1][y * 2 + 1] = Color.RED.value

    def make_shortest_path(self, path: list[tuple[int, int]]) -> None:
        if not path:
            return

        for i in range(len(path)):
            x, y = path[i]
            self._visual[x * 2 + 1][y * 2 + 1] = Color.BLUE.value
            if i > 0:
                prev_x, prev_y = path[i - 1]
                road_x = x + prev_x + 1
                road_y = y + prev_y + 1
                self._visual[road_x][road_y] = Color.BLUE.value

    def show_simple(self):
        for y in range(self._config.HEIGHT * 2 + 1):
            for x in range(self._config.WIDTH * 2 + 1):
                print(self._visual[x][y], end="")
            print()

    # def show_animation(self):


    def show(self) -> None:
        os.system('clear')
        self.show_simple()
        print("=== A-Maze-ing ===")
        print("1. Re-generate a new maze")
        print("2. Show / Hide the shortest path")
        print("3. Rotate the wall colors")
        print("4. Quit")
        choice = input("Choice? (1-4): ")
        if int(choice) == 1:
            self.show()
        if int(choice) == 2:
            self._show_path = not self._show_path
            self.visualize()
            self.show()
        if int(choice) == 3:
            self.change_color()
            self.visualize()
            self.show()
        if int(choice) == 4:
            return

    def change_color(self) -> None:
        class CustomColor:
            def __init__(self, val):
                self.value = val

        val = self._wall_color.value

        if val == Color.WHITE.value:
            self._wall_color = Color.GREEN
        elif val == Color.GREEN.value:
            self._wall_color = Color.YELLOW
        elif val == Color.YELLOW.value:
            self._wall_color = Color.MAGENTA
        elif val == Color.MAGENTA.value:
            self._wall_color = Color.CYAN
        elif val == Color.CYAN.value:
            self._wall_color = Color.BRIGHT_RED
        elif val == Color.BRIGHT_RED.value:
            self._wall_color = Color.BRIGHT_GREEN
        elif val == Color.BRIGHT_GREEN.value:
            self._wall_color = Color.BRIGHT_YELLOW
        elif val == Color.BRIGHT_YELLOW.value:
            self._wall_color = Color.BRIGHT_MAGENTA
        elif val == Color.BRIGHT_MAGENTA.value:
            self._wall_color = Color.BRIGHT_CYAN
        elif val == Color.BRIGHT_CYAN.value:
            self._wall_color = CustomColor("\033[48;5;17m  \033[0m")
        elif val == "\033[48;5;17m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;18m  \033[0m")
        elif val == "\033[48;5;18m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;19m  \033[0m")
        elif val == "\033[48;5;19m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;20m  \033[0m")
        elif val == "\033[48;5;20m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;21m  \033[0m")
        elif val == "\033[48;5;21m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;22m  \033[0m")
        elif val == "\033[48;5;22m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;23m  \033[0m")
        elif val == "\033[48;5;23m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;24m  \033[0m")
        elif val == "\033[48;5;24m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;25m  \033[0m")
        elif val == "\033[48;5;25m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;26m  \033[0m")
        elif val == "\033[48;5;26m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;27m  \033[0m")
        elif val == "\033[48;5;27m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;28m  \033[0m")
        elif val == "\033[48;5;28m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;29m  \033[0m")
        elif val == "\033[48;5;29m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;30m  \033[0m")
        elif val == "\033[48;5;30m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;31m  \033[0m")
        elif val == "\033[48;5;31m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;32m  \033[0m")
        elif val == "\033[48;5;32m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;33m  \033[0m")
        elif val == "\033[48;5;33m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;34m  \033[0m")
        elif val == "\033[48;5;34m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;35m  \033[0m")
        elif val == "\033[48;5;35m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;36m  \033[0m")
        elif val == "\033[48;5;36m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;37m  \033[0m")
        elif val == "\033[48;5;37m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;38m  \033[0m")
        elif val == "\033[48;5;38m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;39m  \033[0m")
        elif val == "\033[48;5;39m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;40m  \033[0m")
        elif val == "\033[48;5;40m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;41m  \033[0m")
        elif val == "\033[48;5;41m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;42m  \033[0m")
        elif val == "\033[48;5;42m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;43m  \033[0m")
        elif val == "\033[48;5;43m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;44m  \033[0m")
        elif val == "\033[48;5;44m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;45m  \033[0m")
        elif val == "\033[48;5;45m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;46m  \033[0m")
        elif val == "\033[48;5;46m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;47m  \033[0m")
        elif val == "\033[48;5;47m  \033[0m":
            self._wall_color = CustomColor("\033[48;5;48m  \033[0m")
        elif val == "\033[48;5;48m  \033[0m":
            self._wall_color = Color.WHITE
        else:
            self._wall_color = Color.WHITE


if __name__ == "__main__":
    print("= Color Test =")
    print(f"{Color.WHITE.value}", end = "")
    print(f"{Color.BLACK.value}", end = "")
    print(f"{Color.BLUE.value}", end = "")
    print(f"{Color.RED.value}", end = "")
    print()

    print('= Visual Test =')
    maze = MazeGenerator()
    print("= 迷路生成前 =")
    maze.maze_show()
    print("= 迷路生成後（バックトラッキング） =")
    maze.maze_gen()
    maze.maze_show()
    print("= 最小経路探索（幅優先）=")
    bfs = BreadthFirstSearch(maze._pos, maze._config)
    bfs.search_maze()
    print("= ビジュアライズテスト =")
    visualizer = Visualizer(bfs._pos, bfs._config, bfs._path)
    visualizer.visualize()
    visualizer.show()
