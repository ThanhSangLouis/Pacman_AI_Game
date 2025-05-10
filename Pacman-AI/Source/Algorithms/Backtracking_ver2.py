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

def is_goal(_map, pos):
    r, c = pos
    return _map[r][c] == FOOD

# AC-3 đơn giản hóa: loại bỏ các bước chắc chắn vi phạm khỏi domain ban đầu
def prune_domain_with_ac3(start_pos, _map, N, M):
    domain = DDX.copy()
    pruned = []
    r, c = start_pos
    for move in DDX:
        dr, dc = move
        nr, nc = r + dr, c + dc
        if not isValid(_map, nr, nc, N, M):
            pruned.append(move)
    for move in pruned:
        domain.remove(move)
    print("✅ AC-3 pruned domain:", domain)
    return domain

def Backtracking_ver2(_map, start_pos, N, M):
    result_path = []
    visited = set()
    domain = prune_domain_with_ac3(start_pos, _map, N, M)

    def backtrack(current_moves, current_pos):
        nonlocal result_path

        if len(current_moves) > MAX_DEPTH:
            return False

        r, c = current_pos
        if (r, c) in visited:
            return False

        visited.add((r, c))

        if is_goal(_map, current_pos):
            result_path = simulate_path(start_pos, current_moves)
            return True

        for dr, dc in domain:
            nr, nc = r + dr, c + dc
            if isValid(_map, nr, nc, N, M):
                if backtrack(current_moves + [(dr, dc)], (nr, nc)):
                    return True

        visited.remove((r, c))
        return False

    backtrack([], start_pos)

    print("✅ Final path returned by Backtracking + AC-3:", result_path)
    return [[r, c] for r, c in result_path[1:]] if len(result_path) > 1 else []
