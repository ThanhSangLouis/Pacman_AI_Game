from constants import FOOD, EMPTY, WALL

DDX = [[0, 1], [0, -1], [1, 0], [-1, 0]] # Chứa các hướng di chuyển cơ bản
# [0,1]: phải [0,-1]: trái [1,0]: xuống [-1,0]: lên

# Kiểm tra xem một ô trên bản đồ có hợp lệ để di chuyển hay không
def isValid(_map, row: int, col: int, N: int, M: int) -> bool:
    return 0 <= row < N and 0 <= col < M and (_map[row][col] == FOOD or _map[row][col] == EMPTY)

# Kiểm tra xem một ô trên bản đồ có hợp lệ để di chuyển nhưng không phải là tường
def isValid2(_map, row: int, col: int, N: int, M: int) -> bool:
    return 0 < row < N and 0 < col < M and _map[row][col] != WALL

# Tính khoảng cách Manhattan giữa hai điểm trên bản đồ.
def Manhattan(x1: int, y1: int, x2: int, y2: int) -> float:
    return abs(x1 - x2) + abs(y1 - y2)

# Tìm thức ăn gần nhất từ vị trí hiện tại của Pac-Man
def find_nearest_food(_food_Position: list[list[int]], start_row: int, start_col: int):
    food_row, food_col = -1, -1  # Ban đầu, chưa tìm thấy thức ăn nào
    for idx in range(len(_food_Position)): 
        if food_row == -1:  # Nếu chưa tìm thấy thức ăn nào
            [food_row, food_col] = _food_Position[idx] 
        elif Manhattan(food_row, food_col, start_row, start_col) > Manhattan(_food_Position[idx][0],
                                                                             _food_Position[idx][1], start_row,
                                                                             start_col):
            [food_row, food_col] = _food_Position[idx]  # Cập nhật vị trí với thức ăn gần hơn
    return food_row, food_col  # Trả về chỉ food_row và food_col

def randomPacManNewPos(_map, row, col, _N, _M):
    for [d_r, d_c] in DDX:
        new_r, new_c = row + d_r, col + d_c
        if isValid2(_map, new_r, new_c, _N, _M):
            return [new_r, new_c]
    return [row, col]
