from Utils.utils import isValid, DDX, Manhattan

def BeamSearch(_map, food_pos, row, col, N, M, beam_width=500):
    if not food_pos:
        return []

    # Choose the nearest food
    goal = min(food_pos, key=lambda f: Manhattan(row, col, f[0], f[1]))
    
    # Track states with their paths to avoid revisiting states with worse paths
    state_best_cost = {}  # (r, c) -> best cost so far
    
    # Each element in beam is (position, path, cost)
    # Where cost is used for sorting, and path is the history
    beam = [([row, col], [[row, col]], 0)]
    
    max_iterations = N * M * 4  # Safety limit to prevent infinite loops
    iterations = 0
    
    while beam and iterations < max_iterations:
        iterations += 1
        candidates = []
        
        for (r, c), path, cost in beam:
            # If we've reached the goal, return the path
            if [r, c] == goal:
                return path
                
            for d_r, d_c in DDX:
                new_r, new_c = r + d_r, c + d_c
                
                if isValid(_map, new_r, new_c, N, M):
                    # Calculate a new cost that factors in both path length and distance to goal
                    new_cost = len(path) + Manhattan(new_r, new_c, goal[0], goal[1])
                    
                    # Skip if we've seen this state with a better cost
                    state_key = (new_r, new_c)
                    if state_key in state_best_cost and state_best_cost[state_key] <= new_cost:
                        continue
                    
                    # Avoid immediate cycles (going back and forth)
                    if len(path) >= 2 and [new_r, new_c] == path[-2]:
                        continue
                    
                    # Update best cost for this state
                    state_best_cost[state_key] = new_cost
                    
                    # Create new path and add to candidates
                    new_path = path + [[new_r, new_c]]
                    candidates.append(([new_r, new_c], new_path, new_cost))
        
        if not candidates:
            break
        
        # Sort candidates by cost (path length + distance to goal)
        candidates.sort(key=lambda x: x[2])
        
        # Keep only the best candidates according to beam width
        beam = candidates[:beam_width]
    
    # If we exit the loop without finding a path, return empty
    return []