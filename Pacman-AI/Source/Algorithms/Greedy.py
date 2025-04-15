
from Utils.utils import DDX, isValid, Manhattan
from collections import deque

def Greedy(_map, food_pos, row, col, N, M):
    if not food_pos or len(food_pos) == 0:
        return []

    goal = food_pos[0]
    visited = [[False for _ in range(M)] for _ in range(N)]
    trace = [[[-1, -1] for _ in range(M)] for _ in range(N)]
    queue = deque()
    queue.append((row, col))
    visited[row][col] = True

    while queue:
        current = queue.popleft()
        if list(current) == goal or _map[current[0]][current[1]] == 2:
            # Truy vết đường đi
            path = [[current[0], current[1]]]
            r, c = current
            while trace[r][c] != [-1, -1]:
                r, c = trace[r][c]
                path.insert(0, [r, c])
            return path

        neighbors = []
        for d_r, d_c in DDX:
            new_r, new_c = current[0] + d_r, current[1] + d_c
            if isValid(_map, new_r, new_c, N, M) and not visited[new_r][new_c]:
                h = Manhattan(new_r, new_c, goal[0], goal[1])
                neighbors.append((h, new_r, new_c))

        neighbors.sort()
        for _, new_r, new_c in neighbors:
            visited[new_r][new_c] = True
            trace[new_r][new_c] = [current[0], current[1]]
            queue.append((new_r, new_c))

    return []
