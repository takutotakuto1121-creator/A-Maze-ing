#!/usr/bin/env python3
import sys
import random
from mazegen.maze_gen_recursive import MazeGenerator
from mazegen.maze_gen_prims import MazeGeneratorPrims
from mazegen.maze_gen_kruskals import MazeGeneratorKruskals
from mazegen.bfs import BreadthFirstSearch
from mazegen.visualizer import Visualizer


def main() -> None:
    """
    main関数

    STRATEGYによって迷路生成アルゴリズムを切り替える
    """
    if len(sys.argv) < 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    maze = MazeGenerator()
    random.seed(maze._config.SEED)

    if maze._config.STRATEGY == "recursive":
        maze.maze_gen()
        bfs = BreadthFirstSearch(maze._pos, maze._config)
        bfs.search_maze()
        maze.output_to_file(bfs._path_cardinal)
        visualizer = Visualizer(
            bfs._pos, bfs._config, bfs._path, maze._history
        )
        visualizer.visualize()
        visualizer.show()
    elif maze._config.STRATEGY == "prims":
        maze_prims = MazeGeneratorPrims()
        maze_prims.maze_gen()
        bfs_prims = BreadthFirstSearch(
            maze_prims._pos, maze_prims._config
        )
        bfs_prims.search_maze()
        maze_prims.output_to_file(bfs_prims._path_cardinal)
        vis_prims = Visualizer(
            bfs_prims._pos, bfs_prims._config, bfs_prims._path, maze_prims._history
        )
        vis_prims.visualize()
        vis_prims.show()
    elif maze._config.STRATEGY == "kruskals":
        maze_kruskals = MazeGeneratorKruskals()
        maze_kruskals.maze_gen()
        bfs_kruskals = BreadthFirstSearch(
            maze_kruskals._pos, maze_kruskals._config
        )
        bfs_kruskals.search_maze()
        maze_kruskals.output_to_file(bfs_kruskals._path_cardinal)
        vis_kruskals = Visualizer(
            bfs_kruskals._pos, bfs_kruskals._config, bfs_kruskals._path, maze_kruskals._history
        )
        vis_kruskals.visualize()
        vis_kruskals.show()


if __name__ == "__main__":
    # try:
    main()
    # except BaseException as e:
    #     print(f"[Error]{e}")
