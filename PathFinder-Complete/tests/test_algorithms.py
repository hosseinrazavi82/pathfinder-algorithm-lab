"""Behavioral and property-style tests for all three pathfinding algorithms."""

from random import Random

import pytest

from pathfinder.algorithms import ALGORITHMS, astar, bfs, dijkstra, manhattan
from pathfinder.examples import EXAMPLES, example_grid, random_grid
from pathfinder.grid import parse_grid


def test_weighted_detour_shows_difference():
    grid = example_grid("Weighted detour")
    b, d, a = bfs(grid), dijkstra(grid), astar(grid)
    assert (b.distance, b.total_cost) == (6, 14)
    assert (d.distance, d.total_cost) == (8, 8)
    assert (a.total_cost, a.distance) == (8, 8)


@pytest.mark.parametrize("name", list(EXAMPLES))
def test_dijkstra_and_astar_agree_for_every_example(name):
    grid = example_grid(name)
    d = dijkstra(grid)
    a = astar(grid)
    assert (a.found, a.total_cost) == (d.found, d.total_cost)
    for result in (bfs(grid), d, a):
        assert result.explored == len(set(result.visited_order))
        assert result.total_cost == grid.path_cost(result.path)
        if result.found:
            assert result.path[0] == grid.start
            assert result.path[-1] == grid.goal
        else:
            assert result.distance is None
            assert result.total_cost is None


@pytest.mark.parametrize("algorithm", list(ALGORITHMS.values()))
def test_no_route(algorithm):
    result = algorithm(example_grid("No route"))
    assert not result.found
    assert result.path == ()
    assert result.total_cost is None


def test_unweighted_all_paths_same_length():
    grid = parse_grid("S...\n.#..\n...G")
    results = [algorithm(grid) for algorithm in ALGORITHMS.values()]
    assert len({result.distance for result in results}) == 1
    assert len({result.total_cost for result in results}) == 1


def test_manhattan():
    assert manhattan((0, 0), (2, 3)) == 5
    assert manhattan((4, 5), (4, 5)) == 0


def test_randomized_optimality_and_validity():
    rng = Random(123)
    for iteration in range(100):
        grid = random_grid(rows=rng.randint(5, 11), cols=rng.randint(5, 11),
                           wall_probability=rng.uniform(0.0, 0.45), seed=iteration, weighted=True)
        d, a, b = dijkstra(grid), astar(grid), bfs(grid)
        assert (d.found, d.total_cost) == (a.found, a.total_cost)
        assert b.found == d.found
        if d.found:
            assert b.distance <= d.distance
            assert b.total_cost >= d.total_cost
            assert d.total_cost == grid.path_cost(d.path)
            assert a.total_cost == grid.path_cost(a.path)
