# Algorithms and theoretical foundations

PathFinder models a grid as a directed graph `G = (V, E)`. A traversable cell is a vertex. There is a directed edge `u → v` whenever `v` is a walkable, orthogonally adjacent cell. The edge's cost is `cost(v)`, the cost of **entering** the destination cell. The starting vertex contributes no entry cost. All edge costs are between 1 and 9.

## Breadth-First Search (BFS)

```text
queue ← [start]
seen ← {start}
parent[start] ← null
while queue is not empty:
    current ← dequeue_front(queue)
    if current is goal: return reconstruct(parent, goal)
    for each unvisited neighbor:
        seen.add(neighbor)
        parent[neighbor] ← current
        enqueue_back(queue, neighbor)
return unreachable
```

BFS visits graph vertices by nondecreasing number of edges from the start. It therefore minimizes **moves** in an unweighted graph, but not total entry cost when movement weights differ. Time is `O(V + E)` and auxiliary space is `O(V)`.

## Dijkstra's shortest path

```text
distance[start] ← 0
heap ← [(0, start)]
while heap is not empty:
    cost, current ← remove_min(heap)
    if this heap entry is stale: continue
    if current is goal: return cost and path
    for each neighbor:
        candidate ← cost + entry_cost(neighbor)
        if candidate < distance[neighbor]:
            distance[neighbor] ← candidate
            parent[neighbor] ← current
            insert (candidate, neighbor) into heap
return unreachable
```

Dijkstra processes the smallest known tentative cost first and returns the minimum total entry cost for graphs with **nonnegative** edge costs. Our implementation uses a heap with lazy deletion of outdated entries; it does not decrease heap keys in place. Typical runtime: `O((V + E) log V)` with a binary heap; memory: `O(V + E)` in this implementation, accounting for heap entries.

## A* search

A* orders entries by:

```text
f(n) = g(n) + h(n)
g(n) = best known cost from start to n
h(n) = |n.row - goal.row| + |n.col - goal.col|
```

We use **Manhattan distance** as `h`. Because every move changes Manhattan distance by at most 1 and all move costs are at least 1, `h` is both admissible (never overestimates remaining optimal cost) and consistent (`h(u) ≤ cost(u,v) + h(v)`). Under these assumptions, when A* pops the goal with the smallest `f`, that route is optimal. We use a `heapq` priority queue with a monotonically increasing sequence number to break ties reproducibly.

A* can explore substantially fewer cells than Dijkstra when the heuristic is informative, but it is not guaranteed to do so on every map. Worst-case time/space complexity depends on heuristic and graph structure, and may approach Dijkstra-style search effort.

## Reconstructing the route

Whenever an algorithm finds a better route to a neighbor, it records `previous[neighbor] = current`. On reaching the goal, it traces `goal → parent → … → start`, reverses the sequence, and returns a route. The result also records the expansion order for animation.

## A reproducible weighted example

```text
S9...
.###.
...#G
.#...
.....
```

- BFS: **6 moves**, **cost 14**, because it crosses the cost-9 cell.
- Dijkstra: **8 moves**, **cost 8**, avoiding the expensive cell.
- A*: **8 moves**, **cost 8**, also optimal.

The `A*` search expands 9 cells versus 15 in Dijkstra for this example given the project's deterministic neighbor order and tie-breakers. These are observations for this input, not universal guarantees.

## Benchmark caveat

Time values are the median of seven calls to each algorithm, measured with `time.perf_counter_ns()`. On grids this small, execution is often a fraction of a millisecond and easily affected by Python startup effects, CPU scheduling, or caching. Treat time numbers as a teaching aid, not as published performance evidence.
