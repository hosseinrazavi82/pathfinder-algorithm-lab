"""Example maps and reproducible random-map generation."""

from __future__ import annotations

from random import Random

from pathfinder.grid import Grid, Position, parse_grid

EXAMPLES: dict[str, str] = {
    "Weighted detour": """
S9...
.###.
...#G
.#...
.....
""",
    "Maze challenge": """
S...#.......
.##.#.####..
....#....#..
.####.##.#..
......#.....
.####.#.###.
....#.......
.##...#####.
..........G.
""",
    "Open field": """
S...........
............
............
............
............
............
............
...........G
""",
    "No route": """
S.#..
..#..
###..
...#.
....G
""",
}


def example_grid(name: str) -> Grid:
    if name not in EXAMPLES:
        raise ValueError(f"Unknown example: {name}")
    return parse_grid(EXAMPLES[name])


def random_grid(
    rows: int = 10,
    cols: int = 12,
    wall_probability: float = 0.22,
    seed: int = 42,
    weighted: bool = True,
) -> Grid:
    """Generate a reproducible map; a solution is not guaranteed."""
    if not 0 <= wall_probability <= 0.8:
        raise ValueError("Wall probability must be in the range [0, 0.8].")
    rng = Random(seed)
    start, goal = (0, 0), (rows - 1, cols - 1)
    walls: set[Position] = set()
    weights: dict[Position, int] = {}
    for r in range(rows):
        for c in range(cols):
            p = (r, c)
            if p in (start, goal):
                continue
            if rng.random() < wall_probability:
                walls.add(p)
            elif weighted and rng.random() < 0.2:
                weights[p] = rng.randint(2, 9)
    return Grid(rows, cols, start, goal, frozenset(walls), weights)
