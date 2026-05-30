"""
Dijkstra's algorithm for grid-based pathfinding.

Dijkstra explores all reachable cells in order of accumulated cost without
a heuristic. On uniform-cost grids it is optimal but typically slower than
A* because it expands more nodes. It is included here as a comparison
baseline to demonstrate the added efficiency of the heuristic in A*.
"""
from __future__ import annotations
import time
from firedrones.environment.grid import Grid
from firedrones.utils.priority_queue import PriorityQueue


class DijkstraPlanner:
    """
    Computes shortest paths on a Grid using Dijkstra's algorithm.

    Unlike A*, Dijkstra does not use a heuristic — it expands cells in
    strict order of their distance from the start. The resulting path
    is identical to A* on a uniform-cost grid, but more cells are
    visited during the search.
    """

    def __init__(self, grid: Grid) -> None:
        self.grid = grid
        self.last_nodes_expanded: int = 0
        self.last_elapsed_ms: float = 0.0

    def find_path(
        self,
        start: tuple[int, int],
        goal: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """
        Find the shortest path from start to goal.

        Args:
            start: (col, row) of the starting cell.
            goal:  (col, row) of the target cell.

        Returns:
            A list of (col, row) positions from start (exclusive) to goal
            (inclusive), or an empty list if no path exists.
        """
        started_at = time.perf_counter()
        self.last_nodes_expanded = 0
        self.last_elapsed_ms = 0.0

        def finish(path: list[tuple[int, int]]) -> list[tuple[int, int]]:
            self.last_elapsed_ms = (time.perf_counter() - started_at) * 1000.0
            return path

        sc, sr = start
        gc, gr = goal

        if not self.grid.in_bounds(sc, sr) or not self.grid.in_bounds(gc, gr):
            return finish([])
        if not self.grid.is_traversable(sc, sr) or not self.grid.is_traversable(gc, gr):
            return finish([])
        if start == goal:
            return finish([])

        open_set: PriorityQueue[tuple[int, int]] = PriorityQueue()
        open_set.push(start, 0.0)

        came_from: dict[tuple[int, int], tuple[int, int] | None] = {start: None}
        dist: dict[tuple[int, int], float] = {start: 0.0}

        while not open_set.empty():
            current = open_set.pop()
            self.last_nodes_expanded += 1
            cc, cr = current

            if current == goal:
                return finish(self._reconstruct(came_from, goal))

            for neighbour in self.grid.neighbours(cc, cr):
                nc, nr = neighbour.col, neighbour.row
                npos = (nc, nr)
                new_dist = dist[current] + 1.0

                if npos not in dist or new_dist < dist[npos]:
                    dist[npos] = new_dist
                    came_from[npos] = current
                    open_set.push(npos, new_dist)

        return finish([])

    @staticmethod
    def _reconstruct(
        came_from: dict[tuple[int, int], tuple[int, int] | None],
        goal: tuple[int, int],
    ) -> list[tuple[int, int]]:
        """Reconstruct the path by following came_from pointers."""
        path: list[tuple[int, int]] = []
        node: tuple[int, int] | None = goal
        while node is not None and came_from.get(node) is not None:
            path.append(node)
            node = came_from[node]
        path.reverse()
        return path
