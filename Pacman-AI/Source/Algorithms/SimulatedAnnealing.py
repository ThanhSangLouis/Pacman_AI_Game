import math
import random
from Utils.utils import DDX, isValid2, Manhattan
from constants import FOOD, MONSTER, WALL

# Hàm cập nhật bản đồ đánh giá nguy hiểm / an toàn dựa trên vị trí thức ăn (FOOD) và quái (MONSTER)
def update_heuristic(_map, current_row, current_col, N, M, depth, visited, _type, heuristic_map):
    visited.append((current_row, current_col)) # Thêm ô hiện tại vào danh sách đã thăm để tránh lặp lại
    
    # Dừng đệ quy khi độ sâu đạt giới hạn
    if depth < 0:
        return
        
    # Khởi tạo điểm ảnh hưởng
    point = 0
    # Nếu là FOOD, giá trị tăng dần khi gần thức ăn
    if _type == FOOD:
        if depth == 2:
            point = 35
        elif depth == 1:
            point = 10
        elif depth == 0:
            point = 5
    # Nếu là MONSTER, giá trị giảm mạnh (hoặc vô cực âm) để tránh quái vật
    elif _type == MONSTER:
        if depth in [2, 1]:
            point = float('-inf')
        elif depth == 0:
            point = -100
            
    heuristic_map[current_row][current_col] += point # Ô hiện tại sẽ cộng thêm point tương ứng
    
    # Duyệt qua các ô lân cận
    for d_r, d_c in DDX:
        new_r, new_c = current_row + d_r, current_col + d_c
        # Nếu ô hợp lệ và chưa được thăm, gọi đệ quy để tiếp tục cập nhật heuristic (depth - 1 per times)
        if isValid2(_map, new_r, new_c, N, M) and (new_r, new_c) not in visited:
            update_heuristic(_map, new_r, new_c, N, M, depth - 1, visited.copy(), _type, heuristic_map)

# Hàm tính tổng điểm cho toàn bộ bản đồ dựa vào vị trí các FOOD & MONSTER
def calc_heuristic(_map, N, M): 
    heuristic_map = [[0 for _ in range(M)] for _ in range(N)]
    visited = []
    
    for r in range(N):
        for c in range(M):
            # Nếu ô là FOOD -> cộng điểm tốt cho các ô xung quanh
            if _map[r][c] == FOOD:
                update_heuristic(_map, r, c, N, M, 2, visited.copy(), FOOD, heuristic_map)
            # Nếu ô là MONSTER -> trừ điểm cho các ô xung quanh
            elif _map[r][c] == MONSTER:
                update_heuristic(_map, r, c, N, M, 2, visited.copy(), MONSTER, heuristic_map)
                
    return heuristic_map

# Hàm tìm hướng đi mới cho PacMan dựa trên bản đồ heuristic
def SimulatedAnnealingForPacMan(_map, start_row, start_col, N, M, _visited, heuristic_map, prev_pos=None, T=1000, stuck_counter=0):
    # Lưu các vị trí gần nhất PacMan đi qua để không bị mắc kẹt trong vòng lặp
    recent_positions = getattr(SimulatedAnnealingForPacMan, 'recent_positions', [])
    if not hasattr(SimulatedAnnealingForPacMan, 'recent_positions'):
        SimulatedAnnealingForPacMan.recent_positions = []
    
    neighbors = []
    # Duyệt các ô lân cận
    for d_r, d_c in DDX:
        new_row, new_col = start_row + d_r, start_col + d_c
        if isValid2(_map, new_row, new_col, N, M) and _map[new_row][new_col] != WALL:
            if heuristic_map[new_row][new_col] != float('-inf'):
                score = heuristic_map[new_row][new_col] - _visited[new_row][new_col] * 2
                
                # Phạt nếu đi ngược lại vị trí trước đó
                if prev_pos and (new_row, new_col) == prev_pos:
                    score -= 100  # Increased penalty
                
                # Giảm điểm nếu ô nằm trong danh sách các vị trí đã đi qua gần đây
                if (new_row, new_col) in recent_positions:
                    penalty = 50 * (len(recent_positions) - recent_positions.index((new_row, new_col)))
                    score -= penalty
                
                # Nếu neighbor chứa thức ăn thì thưởng 200 -> Khuyến khích ăn nhanh
                if _map[new_row][new_col] == FOOD:
                    score += 200
                
                neighbors.append(((new_row, new_col), score))

    # Nếu không neighbor hợp lệ, đứng lại
    if not neighbors:
        return [], (start_row, start_col), T, stuck_counter
    
    # Chọn ngẫu nhiên một neighbor nếu không có neighbor hợp lệ
    if random.random() < 0.1: 
        move = random.choice([pos for pos, _ in neighbors])
    # Chọn neighbor tốt nhất dựa trên điểm số
    else:
        best_neighbor = max(neighbors, key=lambda x: x[1])
        best_score = best_neighbor[1]
        current_score = heuristic_map[start_row][start_col] - _visited[start_row][start_col] * 2
        
        # Nếu điểm số của neighbor tốt hơn điểm số hiện tại -> chọn neighbor đó
        if best_score > current_score:
            move = best_neighbor[0]
            stuck_counter = 0
        # Nếu không, có xác suất chấp nhận move xấu
        else:
            delta = best_score - current_score
            probability = math.exp(delta / T) if T > 0 else 0
            if random.random() < probability: # Nếu số random nhỏ hơn probability -> chấp nhận move xấu
                move = best_neighbor[0]
                stuck_counter = 0
            else:
                # Lọc ra các neighbor chưa bị đi nhiều lần gần đây
                filtered_neighbors = [n for n in neighbors if n[0] not in recent_positions]
                if filtered_neighbors: # Nếu có neighbor -> random chọn
                    move = random.choice(filtered_neighbors)[0]
                else: # Nếu không còn neighbor mới -> random đại.
                    move = random.choice([pos for pos, _ in neighbors])
                stuck_counter += 1
    
    recent_positions = SimulatedAnnealingForPacMan.recent_positions
    recent_positions.append((move[0], move[1]))
    if len(recent_positions) > 5:
        recent_positions.pop(0)
    SimulatedAnnealingForPacMan.recent_positions = recent_positions
    
    _visited[move[0]][move[1]] += 1 # Tăng số lần ghé thăm tại ô vừa move đến
    
    # Nếu Pacman không tìm được nước đi tốt trong 3 lần liên tiếp, tăng nhiệt độ T nhanh hơn -> Giúp Pacman liều hơn
    if stuck_counter >= 3:
        T = max(T * 1.5, 500)
    # Nếu Pacman không bị mắc kẹt, giảm nhiệt độ T từ từ
    else:
        T *= 0.95
    return [list(move)], move, T, stuck_counter