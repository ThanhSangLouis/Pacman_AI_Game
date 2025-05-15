from Utils.utils import DDX, isValid2
from constants import FOOD, MONSTER, WALL


def update_heuristic(_map, start_row, start_col, current_row, current_col, N, M, depth, visited, _type, cost):
    visited.append((current_row, current_col))  # Thêm ô hiện tại vào danh sách đã thăm để tránh lặp lại
    
    if depth < 0: # Tránh đệ quy vô hạn
        return 
    if (start_row, start_col) == (current_row, current_col): # Tránh trỏ vào chính mình
        return

    point = 0
    if _type == FOOD: # Nếu là thức ăn, càng gần điểm càng cao.
        if depth == 2:
            point = 35
        elif depth == 1:
            point = 10
        elif depth == 0:
            point = 5

    elif _type == MONSTER: # Nếu là quái, càng gần điểm càng thấp.
        if depth == 2 or depth == 1:
            point = float("-inf")
        elif depth == 0:
            point = -100

    cost[current_row][current_col] += point #Ghi điểm vào ma trận cost để dùng sau.

    for [d_r, d_c] in DDX: # Duyệt qua các ô lân cận
        new_row, new_col = current_row + d_r, current_col + d_c 
        if isValid2(_map, new_row, new_col, N, M) and (new_row, new_col) not in visited: # Nếu ô hợp lệ và chưa được thăm thì gọi đệ quy để tiếp tục cập nhật heuristic (depth - 1 per times)
            update_heuristic(_map, start_row, start_col, new_row, new_col, N, M, depth - 1, visited.copy(), _type, cost) 

def calc_heuristic(_map, start_row, start_col, current_row, current_col, N, M, depth, visited, cost, _visited):
    visited.append((current_row, current_col))

    if depth <= 0: # Dừng đệ quy khi độ sâu đạt giới hạn
        return

    for [d_r, d_c] in DDX: # Duyệt qua các ô lân cận chưa thăm
        new_row, new_col = current_row + d_r, current_col + d_c
        if isValid2(_map, new_row, new_col, N, M) and (new_row, new_col) not in visited:

            sub_visited = []
            # Nếu phát hiện thức ăn/quái vật thì lan ảnh hưởng heuristic
            if _map[new_row][new_col] == FOOD:
                update_heuristic(_map, start_row, start_col, new_row, new_col, N, M, 2, sub_visited, FOOD, cost)
            elif _map[new_row][new_col] == MONSTER:
                update_heuristic(_map, start_row, start_col, new_row, new_col, N, M, 2, sub_visited, MONSTER, cost)

            calc_heuristic(_map, start_row, start_col, new_row, new_col, N, M, depth - 1, visited.copy(), cost, _visited)  # Đệ quy ra xa hơn

    cost[current_row][current_col] -= _visited[current_row][current_col] # Trừ đi số lần PacMan đã ghé để giảm khả năng quay lại.


def SA_HillClimbing(_map, food_pos, start_row, start_col, N, M, _visited):
    visited = [] 
    # Tạo ma trận cost và cập nhật điểm heuristic với độ sâu 3.
    cost = [[0 for _ in range(M)] for _ in range(N)]
    calc_heuristic(_map, start_row, start_col, start_row, start_col, N, M, 3, visited, cost, _visited) 
    
    # Tìm ô có điểm cao nhất.
    max_f = float("-inf")
    result = []
    
    # Lặp để chọn ô gần nhất có điểm cao và ít đi qua nhất
    for [d_r, d_c] in DDX:
        new_row, new_col = start_row + d_r, start_col + d_c
        if isValid2(_map, new_row, new_col, N, M) and _map[new_row][new_col] != WALL: # Nếu ô hợp lệ và chưa được thăm
            score = cost[new_row][new_col] - _visited[new_row][new_col] # Trừ đi số lần PacMan đã ghé để giảm khả năng quay lại.
            if score > max_f: # Nếu ô này có điểm cao hơn ô trước đó
                max_f = score 
                result = [new_row, new_col]
    return result
