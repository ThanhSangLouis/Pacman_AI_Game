from Utils.utils import DDX, isValid
from constants import FOOD

def Deque_DFS(_map, _food_Position, row, col, N, M, visited, trace, expansions):
    if visited[row][col]:
        return 0
    visited[row][col] = True
    trace.append([row, col])
    expansions[0] += 1  # ✅ Đếm node được mở rộng

    if _map[row][col] == FOOD:
        return 1

    for [d_r, d_c] in DDX:
        new_row, new_col = row + d_r, col + d_c
        if isValid(_map, new_row, new_col, N, M) and not visited[new_row][new_col]:
            res = Deque_DFS(_map, _food_Position, new_row, new_col, N, M, visited, trace, expansions)
            if res == 1:
                return 1
            if trace:
                trace.pop()

    return 0


def DFS(_map, _food_Position, start_row, start_col, N, M):
    visited = [[False for _ in range(M)] for _ in range(N)]
    trace = []
    expansions = [0]  # ✅ Dùng list để truyền tham chiếu

    res = Deque_DFS(_map, _food_Position, start_row, start_col, N, M, visited, trace, expansions)

    if res == 1:
        print(f"✅ DFS: Path found with {len(trace)} steps, {expansions[0]} nodes expanded.")
        return trace  # 👈 Trả lại `trace` để PacMan đi tiếp, không trả `expansions`
    
    print(f"❌ DFS: No path found. {expansions[0]} nodes expanded.")
    return []
