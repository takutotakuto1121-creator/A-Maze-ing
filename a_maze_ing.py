#!/usr/bin/env python3
import sys
from mazegen.maze_gen_recursive import MazeGenerator
from mazegen.maze_gen_prims import MazeGeneratorPrims
from mazegen.maze_gen_kruskals import MazeGeneratorKruskals
from mazegen.bfs import BreadthFirstSearch
from visualizer import Visualizer

def main():
    """
    main関数

    STRATEGYによって迷路生成アルゴリズムを切り替える
    """
    if len(sys.argv) < 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    maze = MazeGenerator()
    if maze._config.STRATEGY == "recursive":
        maze.maze_gen()
        bfs = BreadthFirstSearch(maze._pos, maze._config)
        bfs.search_maze()
        maze.output_to_file(bfs._path)
        visualizer = Visualizer(bfs._pos, bfs._config, bfs._path)
        visualizer.visualize()
        visualizer.show()
    elif maze._config.STRATEGY == "prims":
        maze_prims = MazeGeneratorPrims()
        maze_prims.maze_gen()
        bfs = BreadthFirstSearch(maze_prims._pos, maze_prims._config)
        bfs.search_maze()
        maze_prims.output_to_file(bfs._path)
        visualizer = Visualizer(bfs._pos, bfs._config, bfs._path)
        visualizer.visualize()
        visualizer.show()
    elif maze._config.STRATEGY == "kruskals":
        maze_kruskals = MazeGeneratorKruskals()
        maze_kruskals.maze_gen()
        bfs = BreadthFirstSearch(maze_kruskals._pos, maze_kruskals._config)
        bfs.search_maze()
        maze_kruskals.output_to_file(bfs._path)
        visualizer = Visualizer(bfs._pos, bfs._config, bfs._path)
        visualizer.visualize()
        visualizer.show()


if __name__ == "__main__":
    # try:
        main()
    # except BaseException as e:
    #     print(f"[Error]{e}")
