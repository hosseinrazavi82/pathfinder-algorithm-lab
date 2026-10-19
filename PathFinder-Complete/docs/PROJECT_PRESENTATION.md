# Project presentation — English academic portfolio

## Suggested project title

**PathFinder: Interactive Visualization and Comparison of Graph Search Algorithms**

## Short description (adapt to your own experience)

> PathFinder is a Python-based application that demonstrates how shortest-path algorithms operate on two-dimensional grids. The project implements Breadth-First Search (BFS), Dijkstra's algorithm, and A* search with a Manhattan-distance heuristic. Through an interactive Streamlit interface, users can construct maps, place obstacles, assign traversal costs, visualize visited nodes, animate searches, and compare path length, total cost, and computational effort. The project combines algorithmic thinking, modular software architecture, interface design, and automated testing.

## Technical skills illustrated

- Python, data structures (`deque`, dictionaries, `heapq`)
- Graph modeling and path reconstruction
- Shortest-path algorithms and heuristic search
- Streamlit / Plotly data visualization
- Unit and randomized tests with pytest
- Reproducible experiments and GitHub Actions
- Documentation and reproducible installation

## Main observation

> On a weighted example grid, BFS returned a 6-move path with total cost 14, while Dijkstra and A* returned an 8-move path with total cost 8. This demonstrates that the shortest path by number of moves is not necessarily the minimum-cost path.

## Questions you should be able to answer

1. Why does BFS use a queue, while Dijkstra and A* use a priority queue?
2. What changes when some cells cost more than others?
3. How does the program reconstruct the final path?
4. Why is Manhattan distance suitable for this grid?
5. When is A* guaranteed to be optimal?
6. What do "explored cells" and "median execution time" measure?
7. What tests demonstrate that your algorithms are correct?
8. What did you personally learn, modify, test, and improve?

## Responsible portfolio use

**Before presenting the repository as your project, run it, understand its source code, make meaningful personal improvements, and ensure the description of your contribution is accurate.** Merely uploading code without understanding it is unlikely to be convincing in an admissions discussion. This project is a portfolio supplement, not an accredited certificate or a guarantee of admission.
