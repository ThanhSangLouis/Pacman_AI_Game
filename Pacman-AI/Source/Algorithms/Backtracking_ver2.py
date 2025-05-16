from Utils.utils import DDX, isValid
from constants import FOOD
from collections import deque

MAX_DEPTH = 200  # Giới hạn độ sâu

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

def get_neighbors(pos, _map, N, M):
    r, c = pos
    neighbors = []
    for dr, dc in DDX:
        nr, nc = r + dr, c + dc
        if isValid(_map, nr, nc, N, M):
            neighbors.append((nr, nc))
    return neighbors

def ac3(domains, _map, N, M):
    queue = deque()
    for var in domains:
        for neighbor in get_neighbors(var, _map, N, M):
            queue.append((var, neighbor))

    while queue:
        xi, xj = queue.popleft()
        if revise(domains, xi, xj):
            if not domains[xi]:
                return False
            for xk in get_neighbors(xi, _map, N, M):
                if xk != xj:
                    queue.append((xk, xi))
    return True

def revise(domains, xi, xj):
    revised = False
    to_remove = []
    for x in domains[xi]:
        if not any(True for y in domains[xj] if y != x):
            to_remove.append(x)
            revised = True
    for val in to_remove:
        domains[xi].remove(val)
    return revised

def Backtracking_ver2(_map, start_pos, N, M):
    result_path = []
    visited = set()
    expansions = [0]  # ✅ Đếm node mở rộng

    # Khởi tạo domains ban đầu
    domains = {}
    for r in range(N):
        for c in range(M):
            if isValid(_map, r, c, N, M):
                domains[(r, c)] = DDX.copy()

    if not ac3(domains, _map, N, M):
        print("❌ AC-3 failed to find arc consistency.")
        return []

    def backtrack(current_moves, current_pos):
        nonlocal result_path

        if len(current_moves) > MAX_DEPTH:
            return False

        r, c = current_pos
        if (r, c) in visited:
            return False

        visited.add((r, c))
        expansions[0] += 1  # ✅ Đếm node mở rộng

        if is_goal(_map, current_pos):
            result_path = simulate_path(start_pos, current_moves)
            return True

        for dr, dc in domains.get(current_pos, []):
            nr, nc = r + dr, c + dc
            if isValid(_map, nr, nc, N, M):
                if backtrack(current_moves + [(dr, dc)], (nr, nc)):
                    return True

        visited.remove((r, c))
        return False

    backtrack([], start_pos)

    if result_path:
        print(f"✅ Backtracking + AC-3: Path found with {len(result_path) - 1} steps, {expansions[0]} nodes expanded.")
    else:
        print(f"❌ Backtracking + AC-3: No path found. {expansions[0]} nodes expanded.")

    return [[r, c] for r, c in result_path[1:]] if len(result_path) > 1 else []
