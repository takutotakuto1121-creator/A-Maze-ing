#!/usr/bin/env python3
import sys
from mazegen.maze_gen_recursive import MazeGenerator
from mazegen.bfs import BreadthFirstSearch
from visualizer import Visualizer

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 a_maze_ing.py config.txt")
        sys.exit(1)

    maze = MazeGenerator()
    maze.maze_gen()

    bfs = BreadthFirstSearch(maze._pos, maze._config)
    bfs.search_maze()

    maze.output_to_file()

    visualizer = Visualizer(bfs._pos, bfs._config, bfs._path)
    visualizer.visualize()
    visualizer.show()

if __name__ == "__main__":
    main()
