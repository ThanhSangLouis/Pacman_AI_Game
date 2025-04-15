from queue import PriorityQueue
from Utils.utils import isValid, DDX

def UCS(_map, food_pos, row, col, N, M):
    visited = [[False for _ in range(M)] for _ in range(N)]
    trace = {}
    cost = {}
    from_pos = (row, col)
    to_pos = tuple(food_pos[0])
    q = PriorityQueue()
    cost[from_pos] = 0
    q.put((0, from_pos))

    while not q.empty():
        _, current = q.get()
        r, c = current
        if visited[r][c]:
            continue
        visited[r][c] = True
        if (r, c) == to_pos:
            path = [[r, c]]
            while (r, c) != from_pos:
                r, c = trace[(r, c)]
                path.insert(0, [r, c])
            return path[1] if len(path) > 1 else []

        for [d_r, d_c] in DDX:
            new_r, new_c = r + d_r, c + d_c
            if isValid(_map, new_r, new_c, N, M):
                next_pos = (new_r, new_c)
                new_cost = cost[(r, c)] + 1
                if next_pos not in cost or new_cost < cost[next_pos]:
                    cost[next_pos] = new_cost
                    trace[next_pos] = (r, c)
                    q.put((new_cost, next_pos))
    return []