from Utils.utils import isValid, DDX

def IDS(_map, food_pos, row, col, N, M, max_depth=50, max_nodes=2000):
    if not food_pos or len(food_pos) == 0:
        return []

    goal = food_pos[0]

    for depth_limit in range(1, max_depth + 1):
        visited = [[False for _ in range(M)] for _ in range(N)]
        trace = [[[-1, -1] for _ in range(M)] for _ in range(N)]
        step_counter = [0]
        found = DLS(row, col, goal, depth_limit, visited, trace, _map, N, M, step_counter, max_nodes)
        if found:
            path = []
            r, c = goal
            while [r, c] != [row, col]:
                path.insert(0, [r, c])
                r, c = trace[r][c]
            path.insert(0, [row, col])
            return path
    return []

def DLS(r, c, goal, depth, visited, trace, _map, N, M, step_counter, max_nodes):
    if step_counter[0] > max_nodes:
        return False
    step_counter[0] += 1

    if depth < 0:
        return False
    if [r, c] == goal or _map[r][c] == 2:
        return True

    visited[r][c] = True

    for d_r, d_c in DDX:
        new_r, new_c = r + d_r, c + d_c
        if 0 <= new_r < N and 0 <= new_c < M:
            if not visited[new_r][new_c] and isValid(_map, new_r, new_c, N, M):
                if DLS(new_r, new_c, goal, depth - 1, visited, trace, _map, N, M, step_counter, max_nodes):
                    trace[new_r][new_c] = [r, c]
                    return True
    return False
