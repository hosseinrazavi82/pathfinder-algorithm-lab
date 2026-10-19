"""Correct, deterministic BFS, Dijkstra and A* implementations."""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from heapq import heappop, heappush
from itertools import count

from pathfinder.grid import Grid, Position


@dataclass(frozen=True)
class SearchResult:
    """A complete search record, including the order of expanded cells."""

    algorithm: str
    path: tuple[Position, ...]
    visited_order: tuple[Position, ...]
    total_cost: int | None

    @property
    def found(self) -> bool:
        return bool(self.path)

    @property
    def distance(self) -> int | None:
        return len(self.path) - 1 if self.path else None

    @property
    def explored(self) -> int:
        return len(self.visited_order)


def _reconstruct(previous: dict[Position, Position | None], goal: Position) -> tuple[Position, ...]:
    route: list[Position] = []
    current: Position | None = goal
    while current is not None:
        route.append(current)
        current = previous[current]
    return tuple(reversed(route))


def bfs(grid: Grid) -> SearchResult:
    """Minimize number of moves, not weighted cost (O(V + E))."""
    queue = deque([grid.start])
    previous: dict[Position, Position | None] = {grid.start: None}
    visited: list[Position] = []
    while queue:
        current = queue.popleft()
        visited.append(current)
        if current == grid.goal:
            route = _reconstruct(previous, current)
            return SearchResult("BFS", route, tuple(visited), grid.path_cost(route))
        for neighbor in grid.neighbors(current):
            if neighbor not in previous:
                previous[neighbor] = current
                queue.append(neighbor)
    return SearchResult("BFS", (), tuple(visited), None)


def dijkstra(grid: Grid) -> SearchResult:
    """Minimize total cost for nonnegative edges (O((V + E) log V))."""
    tie_breaker = count()
    heap: list[tuple[int, int, Position]] = [(0, next(tie_breaker), grid.start)]
    best: dict[Position, int] = {grid.start: 0}
    previous: dict[Position, Position | None] = {grid.start: None}
    visited: list[Position] = []
    while heap:
        cost, _, current = heappop(heap)
        if cost != best[current]:
            continue
        visited.append(current)
        if current == grid.goal:
            return SearchResult("Dijkstra", _reconstruct(previous, current), tuple(visited), cost)
        for neighbor in grid.neighbors(current):
            tentative = cost + grid.entry_cost(neighbor)
            if tentative < best.get(neighbor, float("inf")):
                best[neighbor] = tentative
                previous[neighbor] = current
                heappush(heap, (tentative, next(tie_breaker), neighbor))
    return SearchResult("Dijkstra", (), tuple(visited), None)


def manhattan(a: Position, b: Position) -> int:
    """Admissible A* heuristic: min movement cost is 1, 4-way moves only."""
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(grid: Grid) -> SearchResult:
    """A* with Manhattan heuristic; optimal for positive costs >= 1."""
    tie_breaker = count()
    h0 = manhattan(grid.start, grid.goal)
    heap: list[tuple[int, int, int, int, Position]] = [
        (h0, h0, next(tie_breaker), 0, grid.start)
    ]
    best: dict[Position, int] = {grid.start: 0}
    previous: dict[Position, Position | None] = {grid.start: None}
    visited: list[Position] = []
    while heap:
        _, _, _, cost, current = heappop(heap)
        if cost != best[current]:
            continue
        visited.append(current)
        if current == grid.goal:
            return SearchResult("A*", _reconstruct(previous, current), tuple(visited), cost)
        for neighbor in grid.neighbors(current):
            tentative = cost + grid.entry_cost(neighbor)
            if tentative < best.get(neighbor, float("inf")):
                best[neighbor] = tentative
                previous[neighbor] = current
                h = manhattan(neighbor, grid.goal)
                heappush(heap, (tentative + h, h, next(tie_breaker), tentative, neighbor))
    return SearchResult("A*", (), tuple(visited), None)


ALGORITHMS = {"BFS": bfs, "Dijkstra": dijkstra, "A*": astar}
