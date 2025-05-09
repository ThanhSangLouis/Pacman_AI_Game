from Utils.utils import DDX, isValid
from constants import FOOD

MAX_DEPTH = 200  # Giới hạn độ sâu để tránh vô hạn vòng lặp

def simulate_path(start_pos, moves):
    r, c = start_pos
    path = [start_pos]
    for move in moves:
        dr, dc = move
        r += dr
        c += dc
        path.append((r, c))
    return path


def is_valid_path(_map, path, N, M):
    visited = set()
    for r, c in path:
        if not isValid(_map, r, c, N, M):
            return False
        if (r, c) in visited:
            return False
        visited.add((r, c))
    return True


def is_goal(_map, pos):
    r, c = pos
    return _map[r][c] == FOOD


def Backtracking(_map, start_pos, N, M):
    result_path = []

    def backtrack(current_moves):
        nonlocal result_path

        if len(current_moves) > MAX_DEPTH:
            return False

        path = simulate_path(start_pos, current_moves)
        if not is_valid_path(_map, path, N, M):
            return False

        if is_goal(_map, path[-1]):
            result_path = path
            return True

        for dr, dc in DDX:
            if backtrack(current_moves + [(dr, dc)]):
                return True

        return False

    backtrack([])

    # ✅ Debug: xem kết quả thực tế
    print("✅ Final path returned by Backtracking:", result_path)

    # ⚠ Quan trọng: bỏ bước đầu tiên là vị trí hiện tại của Pacman
    return [[r, c] for r, c in result_path[1:]] if len(result_path) > 1 else []
