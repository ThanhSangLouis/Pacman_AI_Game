from queue import PriorityQueue
from Utils.utils import isValid, DDX
from constants import MONSTER

def UCS(_map, food_pos, row, col, N, M):
    visited = [[False for _ in range(M)] for _ in range(N)]
    trace = {}
    cost = {}
    from_pos = (row, col)

    if not food_pos:
        print("❌ UCS: No food provided.")
        return []

    to_pos = tuple(food_pos[0])
    # print(f"🚀 UCS start from {from_pos} to {to_pos}")

    if from_pos == to_pos:
        print("✅ UCS: Already at goal.")
        return []

    # Lấy vị trí ghost
    ghost_pos = []
    for r in range(N):
        for c in range(M):
            if _map[r][c] == MONSTER:
                ghost_pos.append((r, c))
    # print(f"👻 UCS: Found {len(ghost_pos)} ghost(s)")

    q = PriorityQueue()
    q.put((0, from_pos))
    cost[from_pos] = 0

    expansions = 0  # Đếm node mở rộng

    while not q.empty():
        _, current = q.get()
        r, c = current

        if visited[r][c]:
            continue
        visited[r][c] = True
        expansions += 1

        if current == to_pos:
            path = [[r, c]]
            while current != from_pos:
                current = trace[current]
                path.insert(0, list(current))
            print(f"✅ UCS: Path found with {len(path)} steps, {expansions} nodes expanded.")
            print(f"💰 Total cost: {cost[to_pos]}")
            return path

        for d_r, d_c in DDX:
            new_r, new_c = r + d_r, c + d_c
            if not isValid(_map, new_r, new_c, N, M):
                continue

            next_pos = (new_r, new_c)
            g_cost = cost[(r, c)] + 1  # Mặc định mỗi bước = 1

            # Tăng chi phí nếu gần ghost
            for g_r, g_c in ghost_pos:
                dist = abs(new_r - g_r) + abs(new_c - g_c)
                if dist == 0:
                    g_cost += 100  # Chạm ghost
                elif dist == 1:
                    g_cost += 10   # Kề ghost
                elif dist == 2:
                    g_cost += 2    # Gần ghost

            if next_pos not in cost or g_cost < cost[next_pos]:
                cost[next_pos] = g_cost
                trace[next_pos] = (r, c)
                q.put((g_cost, next_pos))

    print(f"❌ UCS: No path found. {expansions} nodes expanded.")
    return []
