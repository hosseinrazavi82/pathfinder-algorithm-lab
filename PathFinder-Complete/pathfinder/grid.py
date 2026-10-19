"""Validated grid representation and compact map parsing."""

from __future__ import annotations

from dataclasses import dataclass, field, replace
from typing import Mapping

Position = tuple[int, int]


@dataclass(frozen=True)
class Grid:
    """A rectangular, four-directional grid with positive entry costs.

    Positions are (row, column), zero indexed. Entering an ordinary cell
    costs 1; entering a weighted cell costs the positive weight shown.
    The starting cell has no entry cost.
    """

    rows: int
    cols: int
    start: Position
    goal: Position
    walls: frozenset[Position] = frozenset()
    weights: Mapping[Position, int] = field(default_factory=dict)

    def __post_init__(self) -> None:
        if not (1 <= self.rows <= 30 and 1 <= self.cols <= 30):
            raise ValueError("Grid dimensions must be between 1 and 30.")
        if self.start == self.goal:
            raise ValueError("Start and goal must be in different cells.")
        for name, position in (("Start", self.start), ("Goal", self.goal)):
            if not self.contains(position):
                raise ValueError(f"{name} lies outside the grid.")
        walls = frozenset(self.walls)
        if not all(self.contains(p) for p in walls):
            raise ValueError("A wall lies outside the grid.")
        if self.start in walls or self.goal in walls:
            raise ValueError("Start and goal cannot be walls.")
        normalized: dict[Position, int] = {}
        for position, weight in self.weights.items():
            if not self.contains(position) or position in walls:
                raise ValueError("Weighted cells must be inside the grid and traversable.")
            if not isinstance(weight, int) or isinstance(weight, bool) or not 1 <= weight <= 9:
                raise ValueError("Cell costs must be integers between 1 and 9.")
            if position != self.start and weight != 1:
                normalized[position] = weight
        object.__setattr__(self, "walls", walls)
        object.__setattr__(self, "weights", normalized)

    def contains(self, position: Position) -> bool:
        row, col = position
        return 0 <= row < self.rows and 0 <= col < self.cols

    def neighbors(self, position: Position) -> tuple[Position, ...]:
        """Return traversable adjacent cells in a reproducible order."""
        row, col = position
        candidates = ((row, col + 1), (row + 1, col), (row, col - 1), (row - 1, col))
        return tuple(p for p in candidates if self.contains(p) and p not in self.walls)

    def entry_cost(self, position: Position) -> int:
        if not self.contains(position) or position in self.walls:
            raise ValueError("Cannot enter an invalid or blocked cell.")
        return self.weights.get(position, 1)

    def path_cost(self, path: tuple[Position, ...]) -> int | None:
        if not path:
            return None
        if path[0] != self.start or path[-1] != self.goal:
            raise ValueError("A path must lead from start to goal.")
        if any(b not in self.neighbors(a) for a, b in zip(path, path[1:])):
            raise ValueError("A path contains an illegal move.")
        return sum(self.entry_cost(position) for position in path[1:])

    def edit(self, position: Position, tool: str, weight: int = 5) -> Grid:
        """Return a new grid after editing one cell (no in-place mutation)."""
        if not self.contains(position):
            raise ValueError("Selected cell is outside the grid.")
        if tool not in {"Wall", "Erase", "Start", "Goal", "Weight"}:
            raise ValueError("Unknown editing tool.")
        walls = set(self.walls)
        weights = dict(self.weights)
        if tool == "Wall":
            if position in (self.start, self.goal):
                raise ValueError("Move the start or goal before blocking this cell.")
            walls.add(position)
            weights.pop(position, None)
        elif tool == "Erase":
            if position in (self.start, self.goal):
                raise ValueError("Move the start or goal before erasing this cell.")
            walls.discard(position)
            weights.pop(position, None)
        elif tool == "Start":
            if position == self.goal:
                raise ValueError("Start and goal cannot overlap.")
            walls.discard(position)
            weights.pop(position, None)
            return replace(self, start=position, walls=frozenset(walls), weights=weights)
        elif tool == "Goal":
            if position == self.start:
                raise ValueError("Start and goal cannot overlap.")
            walls.discard(position)
            weights.pop(position, None)
            return replace(self, goal=position, walls=frozenset(walls), weights=weights)
        elif tool == "Weight":
            if position in (self.start, self.goal):
                raise ValueError("Start and goal cannot be weighted in the editor.")
            if not isinstance(weight, int) or not 2 <= weight <= 9:
                raise ValueError("Choose an integer cost from 2 to 9.")
            walls.discard(position)
            weights[position] = weight
        return replace(self, walls=frozenset(walls), weights=weights)


def parse_grid(text: str) -> Grid:
    """Parse S=start, G=goal, #=wall, .=cost 1 and 1-9=entry cost.

    Blank surrounding lines and indentation are ignored. Interior blank
    lines are rejected to avoid accidentally distorting the map.
    """
    lines = [line.strip() for line in text.strip().splitlines()]
    if not lines or any(not line for line in lines):
        raise ValueError("The map must have nonempty rows.")
    if any(len(line) != len(lines[0]) for line in lines):
        raise ValueError("Every map row must have the same width.")
    walls: set[Position] = set()
    weights: dict[Position, int] = {}
    starts: list[Position] = []
    goals: list[Position] = []
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            p = (r, c)
            if char == "S":
                starts.append(p)
            elif char == "G":
                goals.append(p)
            elif char == "#":
                walls.add(p)
            elif char in ".1":
                continue
            elif char in "23456789":
                weights[p] = int(char)
            else:
                raise ValueError(f"Invalid map symbol {char!r} at row {r + 1}, column {c + 1}.")
    if len(starts) != 1 or len(goals) != 1:
        raise ValueError("A map must contain exactly one S and one G.")
    return Grid(len(lines), len(lines[0]), starts[0], goals[0], frozenset(walls), weights)


def draw_grid(grid: Grid, path: tuple[Position, ...] = ()) -> str:
    """Return a readable ASCII map; preserve start/goal over route symbols."""
    path_cells = set(path)
    output: list[str] = []
    for r in range(grid.rows):
        row: list[str] = []
        for c in range(grid.cols):
            p = (r, c)
            if p == grid.start:
                symbol = "S"
            elif p == grid.goal:
                symbol = "G"
            elif p in grid.walls:
                symbol = "#"
            elif p in path_cells:
                symbol = "*"
            else:
                cost = grid.entry_cost(p)
                symbol = str(cost) if cost > 1 else "."
            row.append(symbol)
        output.append("".join(row))
    return "\n".join(output)
