from Utils.utils import DDX, isValid, Manhattan

def IDAStar(_map, food_pos, row, col, N, M):
    goal = food_pos[0]
    threshold = Manhattan(row, col, goal[0], goal[1])

    def dfs(r, c, g, bound, path):
        f = g + Manhattan(r, c, goal[0], goal[1])
        if f > bound:
            return f
        if [r, c] == goal:
            return "FOUND", path
        min_cost = float("inf")
        for [d_r, d_c] in DDX:
            new_r, new_c = r + d_r, c + d_c
            if isValid(_map, new_r, new_c, N, M) and [new_r, new_c] not in path:
                path.append([new_r, new_c])
                result = dfs(new_r, new_c, g + 1, bound, path)
                if isinstance(result, tuple):
                    return result
                if result < min_cost:
                    min_cost = result
                path.pop()
        return min_cost

    while True:
        result = dfs(row, col, 0, threshold, [[row, col]])
        if isinstance(result, tuple):
            return result[1][1] if len(result[1]) > 1 else []
        if result == float("inf"):
            return []
        threshold = result