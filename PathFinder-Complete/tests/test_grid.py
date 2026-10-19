"""Grid validation and editor behavior."""

import pytest

from pathfinder.grid import Grid, draw_grid, parse_grid


def test_parse_and_draw_round_trip():
    text = "S9.\n.#.\n..G"
    grid = parse_grid(text)
    assert grid.rows == 3 and grid.cols == 3
    assert grid.weights[(0, 1)] == 9
    assert draw_grid(grid) == text


@pytest.mark.parametrize("text", ["", "S.\n.GG", "S..\nG.", "S..\n..G\n...X", "S#G\n.."])
def test_invalid_maps(text):
    with pytest.raises(ValueError):
        parse_grid(text)


def test_neighbors_respect_obstacles():
    grid = parse_grid("S.#\n..G")
    assert grid.neighbors((0, 0)) == ((0, 1), (1, 0))
    assert (0, 2) not in grid.neighbors((0, 1))


def test_editor_wall_weight_erase_and_reposition():
    grid = parse_grid("S...\n....\n...G")
    blocked = grid.edit((0, 1), "Wall")
    assert (0, 1) in blocked.walls
    weighted = blocked.edit((0, 1), "Weight", weight=7)
    assert (0, 1) not in weighted.walls
    assert weighted.weights[(0, 1)] == 7
    blank = weighted.edit((0, 1), "Erase")
    assert (0, 1) not in blank.weights
    moved = blank.edit((1, 1), "Start")
    assert moved.start == (1, 1)
    assert grid.start == (0, 0)


def test_invalid_edits_and_weights():
    grid = parse_grid("S.\n.G")
    with pytest.raises(ValueError):
        grid.edit(grid.start, "Wall")
    with pytest.raises(ValueError):
        grid.edit(grid.goal, "Start")
    with pytest.raises(ValueError):
        grid.edit((0, 1), "Weight", 10)
    with pytest.raises(ValueError):
        Grid(2, 2, (0, 0), (1, 1), weights={(0, 1): 0})


def test_path_cost_validation():
    grid = parse_grid("S9\n.G")
    assert grid.path_cost(((0, 0), (1, 0), (1, 1))) == 2
    assert grid.path_cost(((0, 0), (0, 1), (1, 1))) == 10
    assert grid.path_cost(()) is None
    with pytest.raises(ValueError):
        grid.path_cost(((0, 0), (1, 1)))
