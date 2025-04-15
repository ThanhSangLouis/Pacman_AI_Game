import random
from Utils.utils import DDX, isValid
from constants import FOOD


def hill_simple(_map, food_pos, row, col, N, M):
    for [d_r, d_c] in DDX:
        new_r, new_c = row + d_r, col + d_c
        if isValid(_map, new_r, new_c, N, M):
            return [new_r, new_c]  
    return []


def hill_steepest(_map, food_pos, row, col, N, M):
    best = None
    best_score = -float("inf")
    for [d_r, d_c] in DDX:
        new_r, new_c = row + d_r, col + d_c
        if isValid(_map, new_r, new_c, N, M):
            score = -abs(new_r - food_pos[0][0]) - abs(new_c - food_pos[0][1])
            if score > best_score:
                best_score = score
                best = [new_r, new_c]
    return best if best else []


def hill_random(_map, food_pos, row, col, N, M):
    moves = []
    for [d_r, d_c] in DDX:
        new_r, new_c = row + d_r, col + d_c
        if isValid(_map, new_r, new_c, N, M):
            moves.append([new_r, new_c])
    return random.choice(moves) if moves else []
