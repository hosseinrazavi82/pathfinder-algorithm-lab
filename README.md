[README.md](https://github.com/user-attachments/files/33687564/README.md)
<div align="center">

![PathFinder: Explore the shortest path](assets/banner.svg)

# PathFinder · Algorithm Lab

**An interactive, educational laboratory for graph search and weighted shortest paths.**

`Python 3.11+` · `Streamlit` · `Plotly` · `BFS` · `Dijkstra` · `A*` · `pytest`

[Run locally](#quick-start) · [See the algorithms](#algorithms) · [Deploy online](#deploy-online) · [Project guide](docs/ARCHITECTURE.md)

</div>

---

## Overview

PathFinder is a full-stack *algorithm-visualization project* built around a clean Python search engine and a Streamlit browser interface. Create your own grid, place walls, assign movement costs, set the start and goal, and compare how three graph-search algorithms explore the same map.

**Why this project exists:** the path with the fewest moves is not always the cheapest path. PathFinder makes that distinction visible and measurable.

### Features

- **Three implemented algorithms:** Breadth-First Search (BFS), Dijkstra's shortest path, and A* with Manhattan heuristic.
- **Interactive map editor:** place or erase walls, move the start/goal, assign cell costs from 2–9.
- **Live path visualization:** inspect explored cells and the final route; animate the expansion process.
- **Repeatable experiments:** ready-made examples, reproducible seeded random maps, and custom map text import/export.
- **Comparative analysis:** path length, total entry cost, expanded cells, and illustrative median execution time.
- **Reliability:** input validation, automated tests, and GitHub Actions CI.
- **Two entry points:** an interactive web app and a lightweight command-line application.

## Quick start

### Windows (PowerShell)

1. Install [Python 3.11 or newer](https://www.python.org/downloads/windows/). Check **Add Python to PATH** during installation if offered.
2. Open the extracted `PathFinder-Complete` folder in VS Code and start a new terminal.
3. Install the dependencies:

   ```powershell
   py -m pip install -r requirements.txt
   ```

4. Launch the interactive app:

   ```powershell
   py -m streamlit run app.py
   ```

5. Open the local URL printed by Streamlit (usually `http://localhost:8501`).

> **Shortcut:** On Windows, you can also double-click `RUN-WINDOWS.bat` to install dependencies and start the app. The first launch requires an internet connection for package installation.

### macOS / Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

### Command-line mode

No third-party packages are needed to use the core algorithms:

```powershell
py main.py
py main.py --algorithm astar --example "Maze challenge"
py main.py --file examples/weighted_detour.txt
py main.py --random --rows 10 --cols 12 --density 0.25 --seed 2026
py main.py --help
```

## First experiment: why weighted paths matter

The default map uses `S` for start, `G` for goal, `#` for wall, `.` for normal terrain (cost 1), and digits `2`–`9` for higher entry costs.

```text
S9...
.###.
...#G
.#...
.....
```

| Algorithm | Distance | Total cost | Interpretation |
| --- | ---: | ---: | --- |
| BFS | 6 moves | 14 | Shortest *number of steps*; crosses cost-9 terrain |
| Dijkstra | 8 moves | 8 | Cheapest route; avoids expensive terrain |
| A* | 8 moves | 8 | Also finds cheapest route, guided by a heuristic |

![The shortest route versus the least-cost route](assets/weighted_comparison.png)

For this example, the observed expanded cell counts are 15 (BFS), 15 (Dijkstra) and 9 (A*) with the deterministic traversal rules used in this code. They can differ on other maps. Runtime measurements vary across computers and should not be interpreted as rigorous benchmarking.

### Cost model

- Movement is allowed only **up/down/left/right** (no diagonals).
- Each cell has an **entry cost** of at least 1.
- Entering a digit cell costs its digit value; entering `.` costs 1.
- The starting cell contributes **zero** entry cost.
- A route is displayed with `*`, while the original map remains preserved in memory.
- Dijkstra and A* minimize the *sum of entry costs*; BFS minimizes *number of moves*.

## How to use the web app

1. Pick a **sample map**, generate a random map, or paste your own map using the sidebar.
2. Expand **Edit the map**, choose a tool (Wall, Erase, Start, Goal, Weight), and click a cell.
3. Click **Run all algorithms**.
4. Switch **Algorithm to visualize** to compare colored explored cells and the final route.
5. Inspect the **results table** and the chart of expanded cells.
6. Click **Animate** to see how the chosen algorithm expands its search.
7. Export the current map as text to reproduce your experiment later.

A map without a valid route is handled gracefully and shown as *unreachable*.

## Algorithms

| Algorithm | Core structure | Optimization objective | Typical complexity |
| --- | --- | --- | --- |
| BFS | FIFO queue | Number of moves | `O(V + E)` |
| Dijkstra | Min-priority queue | Total nonnegative cost | `O((V + E) log V)` |
| A* | Min-priority queue + heuristic | Total cost (with admissible heuristic) | Depends on heuristic and search space; worst-case can resemble Dijkstra |

**A* optimality note:** the Manhattan distance is an admissible and consistent heuristic here because movements are orthogonal and every legal movement has cost **≥ 1**. For this project, A* and Dijkstra should always agree on minimum total cost when a route exists.

Read [ALGORITHMS.md](docs/ALGORITHMS.md) for pseudocode, correctness assumptions, and examples.

## Project structure

```text
PathFinder-Complete/
├── app.py                     # Interactive Streamlit application
├── main.py                    # Command-line runner
├── pathfinder/
│   ├── __init__.py
│   ├── grid.py                 # Grid model, editing, parsing, rendering
│   ├── algorithms.py           # BFS, Dijkstra and A*
│   ├── benchmark.py            # Repeated-run experiment helper
│   └── examples.py             # Presets and deterministic random grids
├── tests/
│   ├── test_grid.py
│   ├── test_algorithms.py
│   └── test_benchmark.py
├── examples/                  # Text-map examples
├── docs/
│   ├── ALGORITHMS.md
│   ├── ARCHITECTURE.md
│   ├── WINDOWS_SETUP.md
│   ├── DEPLOYMENT.md
│   └── PROJECT_PRESENTATION.md
├── assets/                    # GitHub banner and route comparison graphic
├── .streamlit/config.toml
├── .github/workflows/tests.yml
├── requirements.txt
├── requirements-dev.txt
├── RUN-WINDOWS.bat
├── .gitignore
└── LICENSE
```

## Test the application

```powershell
py -m pip install -r requirements-dev.txt
py -m pytest -v
py -m ruff check pathfinder main.py app.py tests
```

The test suite checks known shortest paths, weighted detours, impossible maps, input validation, editor operations, reproducible random maps, and **100 randomized cases** comparing A* to Dijkstra. A green CI run after pushing confirms the tests also pass on GitHub's runners.

## Deploy online

1. Push the **contents** of this folder (not the ZIP file) to a **public GitHub repository**.
2. Sign in to [Streamlit Community Cloud](https://share.streamlit.io/).
3. Create a new app, choose your repository and branch, and set the main file path to **`app.py`**.
4. Deploy. Streamlit will install dependencies from `requirements.txt`.
5. Add the resulting public app URL to the **About** section of your GitHub repository and near the top of this README.

**Important:** this package does not contain a live hosted URL; deployment requires access to your GitHub and Streamlit accounts. See [DEPLOYMENT.md](docs/DEPLOYMENT.md) for click-by-click instructions.

## Learning outcomes

Through PathFinder, the developer can explain:

- Graph representation, vertices and edges, and grid-based neighborhoods.
- Queue versus heap-backed priority queue.
- Path reconstruction with predecessor pointers.
- Search optimality for unweighted versus weighted graphs.
- The admissibility and consistency of the Manhattan heuristic.
- Algorithm testing, reproducibility, and performance measurement.
- Separation of concerns between user interface and algorithm engine.

An English project summary for an academic portfolio is provided in [PROJECT_PRESENTATION.md](docs/PROJECT_PRESENTATION.md). Read and understand the code and add your own experiments before representing it as personal coursework or original independent work.

## Limitations and future directions

- Costs are **positive integers 1–9**; this project does not implement negative weights.
- Grids support **4-directional movement**, not diagonal or geographic routing.
- Search animations replay recorded expansion order; they do not capture each intermediate priority-queue state.
- Runtime estimates are educational (small sample sizes, no warm-up/CPU isolation).
- Large grids are capped at 30×30 in the engine; the visual editor uses up to 14×14 for usability.

Possible extensions: bidirectional search, more heuristics, maze-generation algorithms, map persistence, and improved benchmark methodology.

## License

MIT License — see [LICENSE](LICENSE).
