
from Utils.utils import DDX, isValid, Manhattan
from collections import deque

def BeamSearch(_map, food_pos, row, col, N, M, beam_width=5):
    if not food_pos or len(food_pos) == 0:
        return []

    goal = food_pos[0]  # chọn 1 điểm thức ăn gần nhất hoặc đầu tiên
    visited = [[False for _ in range(M)] for _ in range(N)]
    trace = [[[-1, -1] for _ in range(M)] for _ in range(N)]

    beam = [[row, col]]
    visited[row][col] = True

    while beam:
        candidates = []
        for r, c in beam:
            for d_r, d_c in DDX:
                new_r, new_c = r + d_r, c + d_c
                if isValid(_map, new_r, new_c, N, M) and not visited[new_r][new_c]:
                    visited[new_r][new_c] = True
                    trace[new_r][new_c] = [r, c]
                    candidates.append([new_r, new_c])

                    if [new_r, new_c] == goal or _map[new_r][new_c] == 2:
                        # Truy vết đường đi
                        path = [[new_r, new_c]]
                        pr, pc = r, c
                        while pr != -1 and pc != -1:
                            path.insert(0, [pr, pc])
                            pr, pc = trace[pr][pc]
                        return path  # Trả về toàn bộ đường đi

        if not candidates:
            break

        # Ưu tiên theo heuristic: h(n) = Manhattan đến goal
        candidates.sort(key=lambda pos: Manhattan(pos[0], pos[1], goal[0], goal[1]))
        beam = candidates[:beam_width]

    return []  # không tìm thấy đường đi
