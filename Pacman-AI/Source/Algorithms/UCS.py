from queue import PriorityQueue
from Utils.utils import isValid, DDX
from constants import MONSTER
from math import inf


def UCS(_map, food_pos, row, col, N, M):
    visited = [[False for _ in range(M)] for _ in range(N)]
    trace = {}
    cost = {}
    from_pos = (row, col)
    to_pos = tuple(food_pos[0])

    if from_pos == to_pos:
        return []

    # Thu thập vị trí ghost
    ghost_pos = []
    for r in range(N):
        for c in range(M):
            if _map[r][c] == MONSTER:
                ghost_pos.append((r, c))

    q = PriorityQueue()
    q.put((0, from_pos))
    cost[from_pos] = 0

    while not q.empty():
        _, current = q.get()
        r, c = current

        if visited[r][c]:
            continue
        visited[r][c] = True

        if current == to_pos:
            path = [[r, c]]
            while current != from_pos:
                current = trace[current]
                path.insert(0, list(current))
            return path

        for d_r, d_c in DDX:
            new_r, new_c = r + d_r, c + d_c
            if not isValid(_map, new_r, new_c, N, M):
                continue

            # Bỏ qua ô nếu gần ghost (distance <= 1)
            danger = False
            for g_r, g_c in ghost_pos:
                dist = abs(new_r - g_r) + abs(new_c - g_c)
                if dist <= 1:
                    danger = True
                    break
            if danger:
                continue  # Bỏ ô nguy hiểm

            next_pos = (new_r, new_c)
            new_cost = cost[(r, c)] + 1

            if next_pos not in cost or new_cost < cost[next_pos]:
                cost[next_pos] = new_cost
                trace[next_pos] = (r, c)
                q.put((new_cost, next_pos))

    return []
