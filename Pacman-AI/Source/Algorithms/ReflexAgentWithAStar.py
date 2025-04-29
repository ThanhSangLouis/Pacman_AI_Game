from queue import PriorityQueue
from Utils.utils import DDX, isValid2, Manhattan, find_nearest_food
from constants import FOOD, MONSTER, WALL

# Hàm cập nhật bản đồ đánh giá nguy hiểm / an toàn dựa trên vị trí thức ăn (FOOD) và quái (MONSTER)
def update_heuristic(_map, current_row, current_col, N, M, depth, visited, _type, heuristic_map):
    visited.append((current_row, current_col))
    
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
            
    heuristic_map[current_row][current_col] += point
    
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

def ReflexAgentWithAStar(_map, start_row, start_col, end_row, end_col, N, M, _visited):
    # Lưu các vị trí gần nhất PacMan đi qua để không bị mắc kẹt trong vòng lặp
    recent_positions = getattr(ReflexAgentWithAStar, 'recent_positions', [])
    if not hasattr(ReflexAgentWithAStar, 'recent_positions'):
        ReflexAgentWithAStar.recent_positions = []
    
    # Khởi tạo các biến cho A*
    visited = [[False for _ in range(M)] for _ in range(N)]
    trace = {}  # Lưu vết đường đi để reconstruct đường ngược lại từ end → start
    cost = {} # Lưu g(n): chi phí di chuyển từ start tới node hiện tại
    
    # Tính bản đồ heuristic
    heuristic_map = calc_heuristic(_map, N, M)

    # Khởi tạo A*
    path = []
    queue = PriorityQueue() # A* ưu tiên node có f(n) = g(n) + h(n) nhỏ nhất
    start = (start_row, start_col)
    end = (end_row, end_col)
    
    cost[start] = 0
    # Xác định hàm ước lượng f(n) = g(n) + h(n)
    # Manhattan(start, end): khoảng cách ước lượng tới đích
    queue.put((Manhattan(start_row, start_col, end_row, end_col), start))
    
    # Chạy thuật toán A*
    while not queue.empty():
        current = queue.get()[1] # Lấy ô có chi phí nhỏ nhất ra xử lý
        visited[current[0]][current[1]] = True
        
        # Kiểm tra điều kiện kết thúc
        if current == end:
            # Tạo đường đi
            path.append([current[0], current[1]])
            while current != start:
                current = trace[current]
                path.append([current[0], current[1]])
            path.reverse()
            
            # Cập nhật số lần thăm mỗi ô trên đường đi
            for [r, c] in path:
                _visited[r][c] += 1
                
            # Cập nhật danh sách vị trí gần đây
            if path:
                move = tuple(path[0])
                recent_positions = ReflexAgentWithAStar.recent_positions
                recent_positions.append(move)
                if len(recent_positions) > 5:
                    recent_positions.pop(0)
                ReflexAgentWithAStar.recent_positions = recent_positions
                
            return path
            
        # Xét tất cả các ô lân cận
        for d_r, d_c in DDX:
            new_r, new_c = current[0] + d_r, current[1] + d_c
            if isValid2(_map, new_r, new_c, N, M) and not visited[new_r][new_c] and _map[new_r][new_c] != WALL:
                # Bỏ qua các ô nguy hiểm
                if heuristic_map[new_r][new_c] == float('-inf'):
                    continue
                    
                group = (new_r, new_c)
                
                # Tính g(n) - chi phí đường đi thực từ điểm xuất phát
                # Thêm mức penalty cho các ô đã đi qua nhiều lần (tương tự SimulatedAnnealing)
                g = cost[current] + 1 + _visited[new_r][new_c] * 0.5
                
                # Nếu là ô đã đi qua gần đây, tăng chi phí (tương tự SimulatedAnnealing)
                if (new_r, new_c) in recent_positions:
                    penalty = 1 + (len(recent_positions) - recent_positions.index((new_r, new_c))) * 0.5
                    g += penalty
                
                # Tính h(n) - khoảng cách Manhattan tới FOOD
                h = Manhattan(new_r, new_c, end_row, end_col)
                
                # Thêm ảnh hưởng từ heuristic map để né quái
                # Sử dụng heuristic_map như một thành phần thứ ba của f
                safety_score = heuristic_map[new_r][new_c]
                
                # Ưu tiên ô có thức ăn 
                if _map[new_r][new_c] == FOOD:
                    safety_score += 100
                
                # Tính f(n) = g(n) + h(n) với các thành phần bổ sung
                # Giữ thuật toán A* bằng cách vẫn ưu tiên theo g+h, nhưng điều chỉnh nhẹ để né quái
                f = g + h - (safety_score * 0.9 )  # safety_score ảnh hưởng nhẹ để không mất tính chất A*
                
                # Cập nhật chi phí và đường đi nếu tìm được đường đi tốt hơn
                if group not in cost or g < cost[group]:
                    cost[group] = g
                    queue.put((f, group))
                    trace[group] = current
    
    # Xử lý trường hợp không tìm thấy đường đi
    # Chọn hướng an toàn nhất dựa trên heuristic map
    max_safety = float("-inf")
    best_move = None
    
    for d_r, d_c in DDX:
        new_r, new_c = start_row + d_r, start_col + d_c
        if isValid2(_map, new_r, new_c, N, M) and _map[new_r][new_c] != WALL:
            if heuristic_map[new_r][new_c] != float("-inf"):
                # Kết hợp điểm an toàn và số lần đã thăm
                safety = heuristic_map[new_r][new_c] - _visited[new_r][new_c] * 2
                
                # Phạt nếu ô nằm trong danh sách các vị trí đã đi qua gần đây
                if (new_r, new_c) in recent_positions:
                    penalty = 50 * (len(recent_positions) - recent_positions.index((new_r, new_c)))
                    safety -= penalty
                
                # Thưởng điểm nếu gặp thức ăn
                if _map[new_r][new_c] == FOOD:
                    safety += 200
                
                if safety > max_safety:
                    max_safety = safety
                    best_move = [new_r, new_c]
    
    if best_move:
        _visited[best_move[0]][best_move[1]] += 1
        
        # Cập nhật danh sách vị trí gần đây
        move = tuple(best_move)
        recent_positions = ReflexAgentWithAStar.recent_positions
        recent_positions.append(move)
        if len(recent_positions) > 5:
            recent_positions.pop(0)
        ReflexAgentWithAStar.recent_positions = recent_positions
        
        return [best_move]
    
    return []

# Hàm bọc cho ReflexAgentWithAStar để tìm thức ăn gần nhất
def ReflexAgentWithAStarWrapper(_map, _food_Position, start_row, start_col, N, M, _visited=None):
    food_row, food_col = find_nearest_food(_food_Position, start_row, start_col)
    
    if food_row == -1 or food_col == -1:
        return []
    
    if _visited is None:
        _visited = [[0 for _ in range(M)] for _ in range(N)]
    
    return ReflexAgentWithAStar(_map, start_row, start_col, food_row, food_col, N, M, _visited)