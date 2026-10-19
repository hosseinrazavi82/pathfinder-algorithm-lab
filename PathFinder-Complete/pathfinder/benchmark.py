"""Small reproducible benchmarks for educational comparisons."""

from __future__ import annotations

from dataclasses import dataclass
from statistics import median
from time import perf_counter_ns

from pathfinder.algorithms import ALGORITHMS, SearchResult
from pathfinder.grid import Grid


@dataclass(frozen=True)
class Measurement:
    result: SearchResult
    median_ms: float


def compare(grid: Grid, repeat: int = 7) -> dict[str, Measurement]:
    """Run each algorithm repeatedly; timing is illustrative, not a rigorous benchmark."""
    if not 1 <= repeat <= 100:
        raise ValueError("Repeat count must be between 1 and 100.")
    output: dict[str, Measurement] = {}
    for name, algorithm in ALGORITHMS.items():
        durations: list[float] = []
        result: SearchResult | None = None
        for _ in range(repeat):
            start = perf_counter_ns()
            result = algorithm(grid)
            durations.append((perf_counter_ns() - start) / 1_000_000)
        assert result is not None
        output[name] = Measurement(result, median(durations))
    return output
