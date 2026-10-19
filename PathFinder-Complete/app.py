"""Interactive Streamlit laboratory for comparing graph-search algorithms.

Run locally: streamlit run app.py
"""

from __future__ import annotations

import math
import time

import plotly.graph_objects as go
import streamlit as st

from pathfinder.algorithms import ALGORITHMS, SearchResult
from pathfinder.benchmark import Measurement, compare
from pathfinder.examples import EXAMPLES, example_grid, random_grid
from pathfinder.grid import Grid, Position, draw_grid, parse_grid

st.set_page_config(
    page_title="PathFinder | Algorithm Lab",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
      .block-container { max-width: 1250px; padding-top: 1.5rem; }
      h1, h2, h3 { letter-spacing: -0.035em; }
      [data-testid="stMetricValue"] { font-weight: 750; }
      .subtitle { font-size: 1.07rem; color: #AFC1DE; margin-top: -.6rem; }
      .eyebrow { color: #7FB1FF; font-weight: 700; font-size: .8rem;
        text-transform: uppercase; letter-spacing: .18em; }
      .legend { color: #B7C7DF; font-size: .88rem; line-height: 1.9; }
      .legend code { color: #F0F5FF; }
      div.stButton > button { font-weight: 600; }
    </style>
    """,
    unsafe_allow_html=True,
)


def map_figure(
    grid: Grid,
    visited: set[Position] | None = None,
    path: tuple[Position, ...] = (),
) -> go.Figure:
    """Render a legible grid with layers for walls, weights and search."""
    visited = visited or set()
    path_cells = set(path)
    z: list[list[int]] = []
    labels: list[list[str]] = []
    hover: list[list[str]] = []
    for r in range(grid.rows):
        row_z: list[int] = []
        row_labels: list[str] = []
        row_hover: list[str] = []
        for c in range(grid.cols):
            p = (r, c)
            if p == grid.start:
                category, symbol, label = 5, "S", "Start"
            elif p == grid.goal:
                category, symbol, label = 6, "G", "Goal"
            elif p in grid.walls:
                category, symbol, label = 1, "", "Wall"
            elif p in path_cells:
                category, symbol, label = 3, "●", "Final route"
            elif p in visited:
                category, symbol, label = 2, "·", "Explored"
            elif p in grid.weights:
                category, symbol, label = 4, str(grid.weights[p]), "Weighted cell"
            else:
                category, symbol, label = 0, "", "Open cell"
            row_z.append(category)
            row_labels.append(symbol)
            row_hover.append(f"Row {r + 1}, column {c + 1}<br>{label}<br>Entry cost: {grid.weights.get(p, 1)}")
        z.append(row_z)
        labels.append(row_labels)
        hover.append(row_hover)

    # Discrete color stops for integer categories 0 to 6.
    palette = ["#23324B", "#0A1020", "#5A4CB0", "#3B98E8", "#E8AB4A", "#1ABF98", "#FC7185"]
    stops = []
    for i, color in enumerate(palette):
        left = max(0.0, (i - 0.5) / 6)
        right = min(1.0, (i + 0.5) / 6)
        stops.extend([[left, color], [right, color]])
    fig = go.Figure(
        go.Heatmap(
            z=z,
            x=list(range(1, grid.cols + 1)),
            y=list(range(1, grid.rows + 1)),
            text=labels,
            texttemplate="%{text}",
            textfont={"size": max(11, 21 - max(grid.rows, grid.cols) // 2), "color": "#FFFFFF"},
            customdata=hover,
            hovertemplate="%{customdata}<extra></extra>",
            colorscale=stops,
            zmin=0,
            zmax=6,
            showscale=False,
            xgap=3,
            ygap=3,
        )
    )
    fig.update_layout(
        height=max(320, min(700, grid.rows * 44 + 65)),
        margin={"l": 15, "r": 15, "t": 12, "b": 15},
        paper_bgcolor="#0B1220",
        plot_bgcolor="#0B1220",
        font={"color": "#B9C9E3"},
        dragmode=False,
    )
    fig.update_xaxes(
        showgrid=False,
        side="top",
        tickmode="linear",
        dtick=1,
        range=[0.5, grid.cols + 0.5],
        fixedrange=True,
        zeroline=False,
    )
    fig.update_yaxes(
        showgrid=False,
        autorange="reversed",
        tickmode="linear",
        dtick=1,
        range=[grid.rows + 0.5, 0.5],
        scaleanchor="x",
        scaleratio=1,
        fixedrange=True,
        zeroline=False,
    )
    return fig


def performance_figure(results: dict[str, Measurement]) -> go.Figure:
    names = list(results)
    values = [results[name].result.explored for name in names]
    fig = go.Figure(
        go.Bar(
            x=names,
            y=values,
            marker_color=["#839CF4", "#41BFD0", "#65DCAB"],
            text=values,
            textposition="outside",
            hovertemplate="%{x}: %{y} explored cells<extra></extra>",
        )
    )
    fig.update_layout(
        title="Explored cells · lower can be better",
        height=320,
        margin={"l": 25, "r": 15, "t": 55, "b": 35},
        paper_bgcolor="#131F33",
        plot_bgcolor="#131F33",
        font={"color": "#E5EDFC"},
        yaxis={"gridcolor": "#2D405A", "rangemode": "tozero"},
        xaxis={"showgrid": False},
        showlegend=False,
    )
    return fig


def set_grid(grid: Grid) -> None:
    st.session_state.grid = grid
    st.session_state.analysis = None


if "grid" not in st.session_state:
    st.session_state.grid = example_grid("Weighted detour")
if "analysis" not in st.session_state:
    st.session_state.analysis = None

with st.sidebar:
    st.markdown("### 🧭 PathFinder Lab")
    st.caption("Build maps. Run searches. Compare evidence.")
    st.divider()
    st.markdown("#### Load a sample")
    preset = st.selectbox("Example map", list(EXAMPLES), label_visibility="collapsed")
    if st.button("Load selected example", use_container_width=True):
        set_grid(example_grid(preset))
        st.rerun()
    st.divider()
    st.markdown("#### Generate a map")
    rows = st.slider("Rows", 5, 14, 10)
    cols = st.slider("Columns", 5, 14, 12)
    density = st.slider("Wall density", 0.0, 0.55, 0.20, 0.05)
    seed = st.number_input("Random seed", value=42, step=1)
    weighted = st.checkbox("Add weighted cells", value=True)
    if st.button("Generate random map", use_container_width=True):
        set_grid(random_grid(rows, cols, density, int(seed), weighted))
        st.rerun()
    st.divider()
    st.markdown("#### Import a custom map")
    with st.expander("Paste text map"):
        imported = st.text_area("Map characters", value="S9..\n.#..\n...G", height=110,
                                help="Use S for start, G for goal, # for walls, . for open cells and 2–9 for weights.")
        if st.button("Load text map"):
            try:
                set_grid(parse_grid(imported))
                st.rerun()
            except ValueError as error:
                st.error(str(error))

st.markdown('<div class="eyebrow">Computer science · Interactive algorithm visualizer</div>', unsafe_allow_html=True)
st.title("PathFinder  /  Algorithm Lab")
st.markdown(
    '<div class="subtitle">A visual exploration of graph search, weighted shortest paths and algorithmic efficiency.</div>',
    unsafe_allow_html=True,
)

current_grid: Grid = st.session_state.grid
m1, m2, m3, m4 = st.columns(4)
m1.metric("Grid size", f"{current_grid.rows} × {current_grid.cols}")
m2.metric("Obstacles", len(current_grid.walls))
m3.metric("Weighted cells", len(current_grid.weights))
m4.metric("Possible cells", current_grid.rows * current_grid.cols - len(current_grid.walls))

st.markdown("### 01 / Map workspace")
chosen = st.selectbox("Algorithm to visualize", list(ALGORITHMS), index=2)
analysis: dict[str, Measurement] | None = st.session_state.analysis
selected_result: SearchResult | None = analysis[chosen].result if analysis else None
st.plotly_chart(
    map_figure(
        current_grid,
        set(selected_result.visited_order) if selected_result else None,
        selected_result.path if selected_result else (),
    ),
    width="stretch",
    config={"displayModeBar": False},
)
st.markdown(
    '<div class="legend">🟢 <code>S</code> Start &nbsp; 🔴 <code>G</code> Goal &nbsp; '
    '⬛ Wall &nbsp; 🟨 Weighted cell (2–9) &nbsp; 🟣 Explored &nbsp; 🔵 Final route</div>',
    unsafe_allow_html=True,
)

with st.expander("✏️ Edit the map — select a tool and click a cell", expanded=False):
    tool, weight_col = st.columns([3, 1])
    with tool:
        editing_tool = st.radio("Editing tool", ["Wall", "Erase", "Start", "Goal", "Weight"],
                                horizontal=True, index=0)
    with weight_col:
        selected_weight = st.slider("Entry cost", 2, 9, 5, disabled=editing_tool != "Weight")
    st.caption("Click any tile below. S/G cannot overlap and cannot be converted directly into walls.")
    for r in range(current_grid.rows):
        cells = st.columns(current_grid.cols, gap="small")
        for c, slot in enumerate(cells):
            p = (r, c)
            if p == current_grid.start:
                label = "🟢"
            elif p == current_grid.goal:
                label = "🔴"
            elif p in current_grid.walls:
                label = "⬛"
            elif p in current_grid.weights:
                label = str(current_grid.weights[p])
            else:
                label = "▫️"
            with slot:
                if st.button(label, key=f"tile-{r}-{c}", use_container_width=True,
                             help=f"Row {r+1}, column {c+1}"):
                    try:
                        set_grid(current_grid.edit(p, editing_tool, selected_weight))
                        st.rerun()
                    except ValueError as error:
                        st.warning(str(error))
    st.download_button(
        "Download this map (.txt)",
        data=draw_grid(current_grid) + "\n",
        file_name="my_map.txt",
        mime="text/plain",
    )

st.markdown("### 02 / Run the experiments")
run_col, info_col = st.columns([1, 3], vertical_alignment="center")
with run_col:
    run_clicked = st.button("▶ Run all algorithms", type="primary", use_container_width=True)
with info_col:
    st.caption("Runs BFS, Dijkstra and A*, each 7 times for an illustrative median runtime.")
if run_clicked:
    st.session_state.analysis = compare(current_grid, repeat=7)
    analysis = st.session_state.analysis
    selected_result = analysis[chosen].result

if analysis is None:
    st.info("Choose or edit a map, then click **Run all algorithms** to display routes and performance.")
else:
    report: list[dict[str, str | int | float]] = []
    for name, measurement in analysis.items():
        item = measurement.result
        report.append({
            "Algorithm": name,
            "Route": "Found" if item.found else "Unreachable",
            "Moves": str(item.distance) if item.found else "—",
            "Total cost": str(item.total_cost) if item.found else "—",
            "Explored cells": item.explored,
            "Median time (ms)": round(measurement.median_ms, 4),
        })
    st.dataframe(report, hide_index=True, use_container_width=True)
    left, right = st.columns([1, 1])
    with left:
        st.plotly_chart(performance_figure(analysis), width="stretch", config={"displayModeBar": False})
    with right:
        st.markdown("#### Findings")
        if analysis["Dijkstra"].result.found:
            optimal_cost = analysis["Dijkstra"].result.total_cost
            st.success(f"Dijkstra and A* find an optimal weighted route with cost **{optimal_cost}**.")
            bfs_cost = analysis["BFS"].result.total_cost
            if bfs_cost is not None and bfs_cost > optimal_cost:
                st.write("BFS chooses fewer *moves* but its route is **more expensive**. This is why weighted pathfinding matters.")
            else:
                st.write("In this map, BFS also happens to find a minimum-cost route.")
            a_explored = analysis["A*"].result.explored
            d_explored = analysis["Dijkstra"].result.explored
            st.write(f"A* explored **{a_explored}** cells; Dijkstra explored **{d_explored}**. Results depend on the map and tie-breaking rules.")
        else:
            st.warning("The goal cannot be reached from the start on this map.")
        st.caption("Times vary by machine and run; the small measurements shown are educational, not a standardized performance benchmark.")

    st.markdown("### 03 / Watch the search")
    anim_col, speed_col = st.columns([1, 2], vertical_alignment="bottom")
    with anim_col:
        animate = st.button(f"▶ Animate {chosen}", use_container_width=True)
    with speed_col:
        delay = st.slider("Delay per frame (seconds)", 0.0, 0.25, 0.04, 0.01)
    if animate:
        result = analysis[chosen].result
        canvas = st.empty()
        progress = st.progress(0)
        steps = result.explored
        skip = max(1, math.ceil(steps / 55))
        frames = list(range(1, steps + 1, skip))
        if frames and frames[-1] != steps:
            frames.append(steps)
        for index, frame in enumerate(frames):
            canvas.plotly_chart(
                map_figure(current_grid, set(result.visited_order[:frame])),
                width="stretch",
                config={"displayModeBar": False},
            )
            progress.progress((index + 1) / len(frames))
            time.sleep(delay)
        canvas.plotly_chart(
            map_figure(current_grid, set(result.visited_order), result.path),
            width="stretch",
            config={"displayModeBar": False},
        )
        st.caption(f"Search complete: {result.explored} expanded cells.")

with st.expander("📚 How the algorithms work"):
    st.markdown(
        """
        **BFS** explores cells in increasing number of moves, using a FIFO queue. It is optimal when every move has equal cost.

        **Dijkstra** explores the smallest known cumulative entry cost, using a priority queue. It finds a minimum-cost path with nonnegative weights.

        **A*** prioritizes `f(n) = g(n) + h(n)`, using the Manhattan distance as its heuristic. Because all entry costs are at least 1 and moves are orthogonal, the heuristic is admissible, so A* also returns a minimum-cost path.

        **Notation:** `V` is the number of traversable cells; `E` is the number of legal moves between them.
        See `docs/ALGORITHMS.md` in the repository for pseudocode and complexity discussions.
        """
    )

st.divider()
st.caption("PathFinder is an educational project. Source code, tests, reproducible examples, and deployment instructions are included in the repository.")
