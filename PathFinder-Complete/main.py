"""Terminal interface: python main.py --help"""

from __future__ import annotations

import argparse

from pathfinder.benchmark import compare
from pathfinder.examples import EXAMPLES, example_grid, random_grid
from pathfinder.grid import draw_grid, parse_grid


def run() -> None:
    parser = argparse.ArgumentParser(description="Compare BFS, Dijkstra and A* on weighted grids.")
    parser.add_argument("--algorithm", choices=["all", "bfs", "dijkstra", "astar"], default="all")
    parser.add_argument("--example", choices=list(EXAMPLES), default="Weighted detour")
    parser.add_argument("--file", help="Path to a custom UTF-8 text map")
    parser.add_argument("--random", action="store_true", help="Generate a random map instead of using an example")
    parser.add_argument("--rows", type=int, default=10)
    parser.add_argument("--cols", type=int, default=12)
    parser.add_argument("--density", type=float, default=0.22)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--unweighted", action="store_true")
    args = parser.parse_args()
    try:
        if args.file:
            with open(args.file, encoding="utf-8") as handle:
                grid = parse_grid(handle.read())
        elif args.random:
            grid = random_grid(args.rows, args.cols, args.density, args.seed, not args.unweighted)
        else:
            grid = example_grid(args.example)
    except (ValueError, OSError) as error:
        parser.error(str(error))

    print("\nPATHFINDER | Intelligent Route Finding\n")
    print(draw_grid(grid))
    print("\nLegend: S=start G=goal #=wall .=normal cell 2-9=entry cost\n")
    measurements = compare(grid)
    selected = {"bfs": "BFS", "dijkstra": "Dijkstra", "astar": "A*"}.get(args.algorithm)
    for name, measurement in measurements.items():
        if selected is not None and name != selected:
            continue
        result = measurement.result
        print(f"{'-' * 45}\n{name}")
        if result.found:
            print(draw_grid(grid, result.path))
            print(f"Moves: {result.distance} | Total cost: {result.total_cost}")
        else:
            print("No route found.")
        print(f"Explored cells: {result.explored} | Median time: {measurement.median_ms:.3f} ms")


if __name__ == "__main__":
    run()
