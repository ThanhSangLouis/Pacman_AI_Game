from Utils.utils import isValid, DDX, Manhattan

def BeamSearch(_map, food_pos, row, col, N, M, beam_width=5):
    if not food_pos:
        return []
    
    goal = min(food_pos, key=lambda f: Manhattan(row, col, f[0], f[1]))
    state_best_cost = {}
    beam = [([row, col], [[row, col]], 0)]

    expansions = 0
    max_iterations = N * M * 4
    iterations = 0

    while beam and iterations < max_iterations:
        iterations += 1
        candidates = []

        for (r, c), path, cost in beam:
            if [r, c] == goal:
                print(f"✅ BeamSearch: Path found with {len(path)} steps, {expansions} nodes expanded.")
                return path

            for d_r, d_c in DDX:
                new_r, new_c = r + d_r, c + d_c

                if isValid(_map, new_r, new_c, N, M):
                    new_cost = Manhattan(new_r, new_c, goal[0], goal[1])
                    state_key = (new_r, new_c)

                    if state_key in state_best_cost and state_best_cost[state_key] <= new_cost:
                        continue

                    if len(path) >= 2 and [new_r, new_c] == path[-2]:
                        continue

                    state_best_cost[state_key] = new_cost
                    new_path = path + [[new_r, new_c]]
                    candidates.append(([new_r, new_c], new_path, new_cost))
                    expansions += 1  # ✅ Đếm node mở rộng

        if not candidates:
            break

        candidates.sort(key=lambda x: x[2])
        beam = candidates[:beam_width]

    print(f"❌ BeamSearch: No path found. {expansions} nodes expanded.")
    return []
