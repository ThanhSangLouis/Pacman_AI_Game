from collections import deque
from constants import MONSTER
from Utils.utils import DDX

def BFS(_map, start_row, start_col, goal_row, goal_col, N, M):
    visited = [[False for _ in range(M)] for _ in range(N)]
    trace = [[[-1, -1] for _ in range(M)] for _ in range(N)]
    queue = deque([(start_row, start_col)])
    visited[start_row][start_col] = True

    expansions = 0  # Đếm số node mở rộng
    AVOID_RADIUS = 0  # 0: né trực tiếp ghost, 1: né xung quanh, -1: không né

    # Thu thập vị trí ghost
    ghost_pos = []
    for r in range(N):
        for c in range(M):
            if _map[r][c] == MONSTER:
                ghost_pos.append((r, c))

    # print(f"🚀 BFS from ({start_row}, {start_col}) to ({goal_row}, {goal_col}), ghost: {len(ghost_pos)}")

    while queue:
        row, col = queue.popleft()
        expansions += 1

        if row == goal_row and col == goal_col:
            path = [[goal_row, goal_col]]
            cur_row, cur_col = goal_row, goal_col
            while True:
                prev_row, prev_col = trace[cur_row][cur_col]
                if prev_row == -1 and prev_col == -1:
                    break
                path.insert(0, [prev_row, prev_col])
                cur_row, cur_col = prev_row, prev_col
            print(f"✅ BFS: Path found with {len(path)} steps, {expansions} nodes expanded.")
            return path

        for d_r, d_c in DDX:
            new_row, new_col = row + d_r, col + d_c

            if not (0 <= new_row < N and 0 <= new_col < M):
                continue
            if _map[new_row][new_col] == 1 or visited[new_row][new_col]:
                continue

            # Né ghost nếu cần
            danger = False
            if AVOID_RADIUS >= 0:
                for g_r, g_c in ghost_pos:
                    dist = abs(new_row - g_r) + abs(new_col - g_c)
                    if dist <= AVOID_RADIUS:
                        danger = True
                        break
            if danger:
                continue

            visited[new_row][new_col] = True
            queue.append((new_row, new_col))
            trace[new_row][new_col] = [row, col]

    print(f"❌ BFS: No path found. {expansions} nodes expanded.")
    return []
