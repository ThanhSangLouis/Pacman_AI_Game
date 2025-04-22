from Utils.utils import DDX, isValid, Manhattan
from queue import PriorityQueue
from constants import MONSTER

def ReflexAgentWithAStar(_map, _food_Position, start_row, start_col, N, M):
    if not _food_Position:
        return []

    # Tìm food gần nhất
    min_dist = float('inf')
    target_food = None
    for food in _food_Position:
        dist = Manhattan(start_row, start_col, food[0], food[1])
        if dist < min_dist:
            min_dist = dist
            target_food = food

    if not target_food:
        return []

    food_row, food_col = target_food

    # Lấy vị trí các ghost
    ghost_positions = []
    for r in range(N):
        for c in range(M):
            if _map[r][c] == MONSTER:
                ghost_positions.append((r, c))

    # A* Search từ (start_row, start_col) -> (food_row, food_col)
    open_set = PriorityQueue()
    open_set.put((0, (start_row, start_col)))

    came_from = {}
    g_score = {(start_row, start_col): 0}

    while not open_set.empty():
        _, current = open_set.get()

        if current == (food_row, food_col):
            # reconstruct path
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.reverse()
            if path:
                return [path[0][0], path[0][1]]  # trả về bước tiếp theo
            else:
                return []

        for d_r, d_c in DDX:
            new_row, new_col = current[0] + d_r, current[1] + d_c
            if not isValid(_map, new_row, new_col, N, M):
                continue

            tentative_g = g_score[current] + 1

            # Phạt nếu gần ghost
            penalty = 0
            for g_r, g_c in ghost_positions:
                dist = Manhattan(new_row, new_col, g_r, g_c)
                if dist == 0:
                    penalty += 1000
                elif dist == 1:
                    penalty += 100
                elif dist == 2:
                    penalty += 10

            tentative_g += penalty

            if (new_row, new_col) not in g_score or tentative_g < g_score[(new_row, new_col)]:
                came_from[(new_row, new_col)] = current
                g_score[(new_row, new_col)] = tentative_g
                f_score = tentative_g + Manhattan(new_row, new_col, food_row, food_col)
                open_set.put((f_score, (new_row, new_col)))

    return []
