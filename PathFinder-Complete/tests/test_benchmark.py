"""Benchmark and random-generator invariants."""

import pytest

from pathfinder.benchmark import compare
from pathfinder.examples import example_grid, random_grid


def test_benchmark_contains_all_algorithms():
    result = compare(example_grid("Weighted detour"), repeat=3)
    assert list(result) == ["BFS", "Dijkstra", "A*"]
    assert all(item.median_ms >= 0 for item in result.values())


def test_benchmark_repetition_validation():
    with pytest.raises(ValueError):
        compare(example_grid("Weighted detour"), repeat=0)


def test_random_map_reproducible_and_valid():
    a = random_grid(seed=888)
    b = random_grid(seed=888)
    assert a == b
    assert a.start not in a.walls
    assert a.goal not in a.walls
    assert set(a.weights).isdisjoint(a.walls)


def test_invalid_random_probability():
    with pytest.raises(ValueError):
        random_grid(wall_probability=0.99)
