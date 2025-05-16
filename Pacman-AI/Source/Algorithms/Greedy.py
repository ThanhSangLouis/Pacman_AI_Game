from queue import PriorityQueue
from Utils.utils import isValid, DDX, Manhattan

def Greedy(_map, food_pos, row, col, N, M):
    if not food_pos:
        return []

    min_h = float('inf')
    goal = None
    for food in food_pos:
        h = Manhattan(row, col, food[0], food[1])
        if h < min_h:
            min_h = h
            goal = food

    if not goal:
        return []

    visited = [[False for _ in range(M)] for _ in range(N)]
    trace = {}
    q = PriorityQueue()
    q.put((Manhattan(row, col, goal[0], goal[1]), (row, col)))
    visited[row][col] = True

    expansions = 0  # ✅ Đếm số node được mở rộng

    while not q.empty():
        _, (r, c) = q.get()
        expansions += 1  # ✅ Cộng mỗi lần lấy node ra

        if [r, c] == goal:
            path = [[r, c]]
            while (r, c) != (row, col):
                r, c = trace[(r, c)]
                path.insert(0, [r, c])
            print(f"✅ Greedy: Path found with {len(path)} steps, {expansions} nodes expanded.")
            return path

        for d_r, d_c in DDX:
            new_r, new_c = r + d_r, c + d_c
            if isValid(_map, new_r, new_c, N, M) and not visited[new_r][new_c]:
                visited[new_r][new_c] = True
                trace[(new_r, new_c)] = (r, c)
                h = Manhattan(new_r, new_c, goal[0], goal[1])
                q.put((h, (new_r, new_c)))

    print(f"❌ Greedy: No path found. {expansions} nodes expanded.")
    return []
