import heapq
from puzzle.base_search import BaseSearch
from puzzle.state import State, GOAL_STATE
from puzzle.result import SearchResult


class AStar(BaseSearch):

    def heuristic(self, state: State) -> int:
        """Distância de Manhattan (admissível e consistente)."""
        total = 0
        for index, tile in enumerate(state.tiles):
            if tile == 0:
                continue
            goal_index = GOAL_STATE.index(tile)
            total += abs(index // 3 - goal_index // 3) + abs(index % 3 - goal_index % 3)
        return total

    def search(self, initial: State) -> SearchResult:
        generated = 1
        expanded = 0
        counter = 0  # desempate estável no heap
        frontier = [(self.heuristic(initial), counter, initial)]
        best_cost = {initial.tiles: initial.cost}
        closed = set()
        max_frontier = 1

        while frontier:
            _, _, current = heapq.heappop(frontier)
            if current.tiles in closed:
                continue
            if current.is_goal:
                return SearchResult(current, expanded, generated, max_frontier, current.cost)
            closed.add(current.tiles)
            expanded += 1
            for child in current.neighbors():
                if child.tiles in closed:
                    continue
                known = best_cost.get(child.tiles)
                if known is not None and known <= child.cost:
                    continue
                best_cost[child.tiles] = child.cost
                generated += 1
                counter += 1
                heapq.heappush(frontier, (child.cost + self.heuristic(child), counter, child))
            max_frontier = max(max_frontier, len(frontier))

        return SearchResult(None, expanded, generated, max_frontier, 0)
