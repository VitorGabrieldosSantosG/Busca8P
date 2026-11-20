from puzzle.base_search import BaseSearch
from puzzle.state import State
from puzzle.result import SearchResult

DEFAULT_DEPTH_LIMIT = 50


class DFS(BaseSearch):

    def __init__(self, depth_limit: int = DEFAULT_DEPTH_LIMIT):
        self.depth_limit = depth_limit

    def search(self, initial: State) -> SearchResult:
        """DFS iterativa com limite de profundidade.

        Mantém o menor custo conhecido para cada estado, de modo que um estado
        só é reexpandido se for alcançado por um caminho mais curto (evita
        ciclos sem perder soluções dentro do limite).
        """
        generated = 1
        expanded = 0
        stack = [initial]
        max_frontier = 1
        best_cost = {initial.tiles: initial.cost}

        while stack:
            current = stack.pop()
            if best_cost.get(current.tiles, current.cost) < current.cost:
                continue  # entrada obsoleta: já há caminho mais curto
            if current.is_goal:
                return SearchResult(current, expanded, generated, max_frontier, current.cost)
            if current.cost >= self.depth_limit:
                continue
            expanded += 1
            # inverte para que a ordem de exploração siga a ordem de neighbors()
            for child in reversed(current.neighbors()):
                known = best_cost.get(child.tiles)
                if known is not None and known <= child.cost:
                    continue
                best_cost[child.tiles] = child.cost
                generated += 1
                stack.append(child)
            max_frontier = max(max_frontier, len(stack))

        return SearchResult(None, expanded, generated, max_frontier, 0)
