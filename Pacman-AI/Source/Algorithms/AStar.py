from queue import PriorityQueue
from Utils.utils import find_nearest_food, Manhattan, DDX, isValid

def AStar(_map, _food_Position, start_row, start_col, N, M):
    visited = [[False for _ in range(M)] for _ in range(N)]
    trace = {}
    cost = {}
    path = []
    queue = PriorityQueue()

    [food_row, food_col] = find_nearest_food(_food_Position, start_row, start_col)
    start = (start_row, start_col)
    end = (food_row, food_col)

    cost[start] = 0
    queue.put((Manhattan(start_row, start_col, food_row, food_col), start))

    expansions = 0  # ✅ Đếm số node mở rộng

    while not queue.empty():
        current = queue.get()[1]
        r, c = current

        if visited[r][c]:
            continue
        visited[r][c] = True
        expansions += 1

        if current == end:
            path.append([r, c])
            while current != start:
                current = trace[current]
                path.insert(0, [current[0], current[1]])
            print(f"✅ A*: Path found with {len(path)} steps, {expansions} nodes expanded.")
            return path

        for d_r, d_c in DDX:
            new_r, new_c = r + d_r, c + d_c
            if isValid(_map, new_r, new_c, N, M) and not visited[new_r][new_c]:
                neighbor = (new_r, new_c)
                g_cost = cost[current] + 1
                f_cost = g_cost + Manhattan(new_r, new_c, food_row, food_col)

                if neighbor not in cost or g_cost < cost[neighbor]:
                    cost[neighbor] = g_cost
                    trace[neighbor] = current
                    queue.put((f_cost, neighbor))

    print(f"❌ A*: No path found. {expansions} nodes expanded.")
    return []
