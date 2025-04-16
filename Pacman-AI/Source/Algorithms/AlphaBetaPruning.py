from Utils.utils import Manhattan, DDX, isValid, isValid2
from constants import FOOD, MONSTER, EMPTY

def evaluationFunction(_map, pac_row, pac_col, N, M, score):
    ghost_distances = []
    food_distances = []
    ghost_positions = []
    
    # Tìm vị trí thức ăn và ma
    for row in range(N):
        for col in range(M):
            if _map[row][col] == FOOD:
                food_distances.append(Manhattan(row, col, pac_row, pac_col))
            elif _map[row][col] == MONSTER:
                ghost_distances.append(Manhattan(row, col, pac_row, pac_col))
                ghost_positions.append((row, col))
    
    # Các trọng số
    WEIGHT_FOOD = 10.0
    WEIGHT_GHOST_DANGER = -15.0
    WEIGHT_PROGRESS = 7.0  # Trọng số cho việc tiến triển
    GHOST_DANGER_ZONE = 3  # Khoảng cách nguy hiểm với ma
    
    INF = 1e9
    eval_score = score
    
    # Kết hợp điểm cho thức ăn
    if food_distances:
        min_food_distance = min(food_distances)
        # Khuyến khích tiếp cận thức ăn
        eval_score += WEIGHT_FOOD / (min_food_distance if min_food_distance > 0 else 1)
        # Bonus cho việc giảm thức ăn còn lại
        eval_score += 3.0 * (N*M - len(food_distances))
    
    # Xử lý ma
    for i, distance in enumerate(ghost_distances):
        if distance <= 0:  # Ma bắt được pacman
            return -INF
            
        # Phạt mạnh nếu ở gần ma
        if distance <= GHOST_DANGER_ZONE:
            # Kiểm tra xem có đường thoát không
            ghost_row, ghost_col = ghost_positions[i]
            is_trapped = True
            
            # Kiểm tra 4 hướng có đường thoát không
            for dr, dc in DDX:
                escape_r, escape_c = pac_row + dr, pac_col + dc
                if isValid(_map, escape_r, escape_c, N, M):
                    # Khoảng cách từ vị trí thoát đến ma
                    escape_distance = Manhattan(escape_r, escape_c, ghost_row, ghost_col)
                    # Nếu vị trí thoát xa ma hơn vị trí hiện tại
                    if escape_distance > distance:
                        is_trapped = False
                        break
            
            # Nếu bị kẹt, phạt nặng hơn
            if is_trapped:
                eval_score += 2 * WEIGHT_GHOST_DANGER / distance
            else:
                eval_score += WEIGHT_GHOST_DANGER / distance
    
    # Khuyến khích khám phá không gian mới thay vì đi qua đi lại
    # Mô phỏng hướng đi tốt để tránh ma và tiếp cận thức ăn
    if food_distances and ghost_distances:
        min_food_pos = None
        min_food_dist = float("inf")
        
        # Tìm thức ăn gần nhất
        for row in range(N):
            for col in range(M):
                if _map[row][col] == FOOD:
                    food_dist = Manhattan(row, col, pac_row, pac_col)
                    if food_dist < min_food_dist:
                        min_food_dist = food_dist
                        min_food_pos = (row, col)
        
        if min_food_pos:
            food_r, food_c = min_food_pos
            
            # Kiểm tra xem ma có ngăn cản đường đi trực tiếp đến thức ăn không
            ghost_blocking = False
            for ghost_r, ghost_c in ghost_positions:
                # Nếu ma nằm giữa pacman và thức ăn
                if (Manhattan(pac_row, pac_col, ghost_r, ghost_c) + 
                    Manhattan(ghost_r, ghost_c, food_r, food_c) <= 
                    min_food_dist + 2):  # +2 là dung sai cho đường đi không thẳng
                    ghost_blocking = True
                    break
            
            # Nếu ma không chặn đường, khuyến khích tiến thẳng đến thức ăn
            if not ghost_blocking:
                eval_score += WEIGHT_PROGRESS
            # Nếu có ma chặn đường, tìm đường đi vòng
            else:
                # Khuyến khích đi ra xa ma đang chặn
                ghost_distances_sum = sum(ghost_distances)
                eval_score += WEIGHT_PROGRESS * (ghost_distances_sum / (len(ghost_distances) * N))
    
    return eval_score

def AlphaBetaAgent(_map, pac_row, pac_col, N, M, depth, Score):
    MAX_DEPTH = min(depth, 2)
    
    # Tìm và lưu vị trí ma và thức ăn
    all_ghosts = []
    all_food = []
    for r in range(N):
        for c in range(M):
            if _map[r][c] == MONSTER:
                all_ghosts.append((r, c))
            elif _map[r][c] == FOOD:
                all_food.append((r, c))
    
    # Lưu lại các vị trí đã đi qua để tránh đi lại
    visited_positions = set()
    
    def get_relevant_ghosts(state, pac_pos, max_ghosts=2):
        """Trả về các ma gần nhất và có khả năng ảnh hưởng đến pacman"""
        r, c = pac_pos
        relevant = []
        ghost_distances = []
        
        for gr, gc in all_ghosts:
            if state[gr][gc] == MONSTER:
                distance = Manhattan(r, c, gr, gc)
                if distance <= 6:  # Chỉ quan tâm ma trong phạm vi 6 ô
                    ghost_distances.append((distance, (gr, gc)))
        
        # Sắp xếp theo khoảng cách và lấy n ma gần nhất
        ghost_distances.sort()
        return [pos for _, pos in ghost_distances[:max_ghosts]]
    
    def is_safe_move(state, r, c, ghosts):
        """Kiểm tra xem nước đi có an toàn không"""
        for gr, gc in ghosts:
            if Manhattan(r, c, gr, gc) <= 1:  # Nguy hiểm nếu ma ở ngay bên cạnh
                return False
        return True
        
    def is_safe_food(state, food_r, food_c, ghosts, safety_threshold=2):
        """Kiểm tra xem thức ăn có an toàn không - Ngưỡng giảm xuống 2"""
        for gr, gc in ghosts:
            if Manhattan(food_r, food_c, gr, gc) <= safety_threshold:
                return False
        return True
        
    def is_path_safe(state, start_r, start_c, end_r, end_c, ghosts, safety_threshold=2):
        """Kiểm tra xem đường đi từ start đến end có an toàn không - Ngưỡng giảm xuống 2"""
        # Đường đi đơn giản theo Manhattan
        # Trong thực tế, có thể dùng BFS hoặc A* để tìm đường đi chính xác
        current_r, current_c = start_r, start_c
        
        # Ước lượng đường đi Manhattan
        while current_r != end_r or current_c != end_c:
            # Di chuyển theo hướng end
            if current_r < end_r:
                current_r += 1
            elif current_r > end_r:
                current_r -= 1
            elif current_c < end_c:
                current_c += 1
            elif current_c > end_c:
                current_c -= 1
                
            # Kiểm tra an toàn tại mỗi điểm trên đường đi
            for gr, gc in ghosts:
                if Manhattan(current_r, current_c, gr, gc) <= safety_threshold:
                    return False
                    
        return True
    
    def find_safe_food(state, pac_r, pac_c, all_ghosts):
        """Tìm thức ăn an toàn gần nhất"""
        SAFETY_THRESHOLD = 2  # Giảm ngưỡng an toàn xuống 2
        PATH_SAFETY = 2      # Giảm ngưỡng an toàn của đường đi xuống 2
        safe_foods = []
        
        for food_r, food_c in all_food:
            if state[food_r][food_c] == FOOD:
                # Kiểm tra xem thức ăn có an toàn không
                if is_safe_food(state, food_r, food_c, all_ghosts, SAFETY_THRESHOLD):
                    # Kiểm tra đường đi có an toàn không
                    if is_path_safe(state, pac_r, pac_c, food_r, food_c, all_ghosts, PATH_SAFETY):
                        distance = Manhattan(pac_r, pac_c, food_r, food_c)
                        safe_foods.append((distance, food_r, food_c))
        
        # Sắp xếp theo khoảng cách
        safe_foods.sort()
        
        return safe_foods
    
    def find_next_move_to_target(state, pac_r, pac_c, target_r, target_c, ghosts):
        """Tìm nước đi tiếp theo để đến mục tiêu"""
        best_move = None
        min_distance = float("inf")
        
        for dr, dc in DDX:
            next_r, next_c = pac_r + dr, pac_c + dc
            if isValid(state, next_r, next_c, N, M):
                # Kiểm tra an toàn
                if is_safe_move(state, next_r, next_c, ghosts):
                    # Tính khoảng cách đến mục tiêu
                    dist = Manhattan(next_r, next_c, target_r, target_c)
                    if dist < min_distance:
                        min_distance = dist
                        best_move = [next_r, next_c]
        
        return best_move
        
    def is_immediate_food(state, pac_r, pac_c):
        """Kiểm tra xem có thức ăn ngay lân cận không"""
        for dr, dc in DDX:
            nr, nc = pac_r + dr, pac_c + dc
            if isValid(state, nr, nc, N, M) and state[nr][nc] == FOOD:
                # Kiểm tra an toàn khi ăn thức ăn này
                if is_safe_move(state, nr, nc, all_ghosts):
                    return [nr, nc]
        return None
    
    def minimax(state, pac_pos, depth_left, score, alpha, beta, is_pacman, ghost_index=0, path_length=0):
        r, c = pac_pos
        
        # Nếu pacman đang ở vị trí của quái vật hoặc hết độ sâu
        if state[r][c] == MONSTER or depth_left == 0:
            return evaluationFunction(state, r, c, N, M, score)
        
        # Kiểm tra xem còn thức ăn không
        food_exists = False
        for fr, fc in all_food:
            if state[fr][fc] == FOOD:
                food_exists = True
                break
        if not food_exists:
            return evaluationFunction(state, r, c, N, M, score)
        
        # Định nghĩa vị trí đã đi qua
        position_key = (r, c, is_pacman, ghost_index, depth_left)
        
        # Phát hiện vòng lặp (đi lại vị trí cũ)
        if path_length > 3 and position_key in visited_positions:
            # Trừ điểm nếu đi lặp lại (khuyến khích tìm đường mới)
            return evaluationFunction(state, r, c, N, M, score) - 5
        
        if is_pacman:  # Lượt của Pacman
            visited_positions.add(position_key)
            max_eval = float("-inf")
            
            # Lấy ma liên quan
            relevant_ghosts = get_relevant_ghosts(state, pac_pos)
            
            # Thử từng hướng di chuyển
            valid_moves = []
            for dr, dc in DDX:
                nr, nc = r + dr, c + dc
                if isValid(state, nr, nc, N, M):
                    valid_moves.append((nr, nc, is_safe_move(state, nr, nc, relevant_ghosts)))
            
            # Sắp xếp nước đi: ưu tiên nước đi an toàn
            valid_moves.sort(key=lambda x: x[2], reverse=True)
            
            for nr, nc, is_safe in valid_moves:
                # Tạo bản sao trạng thái
                new_state = [row[:] for row in state]
                
                # Tính điểm mới
                new_score = score
                if new_state[nr][nc] == FOOD:
                    new_score += 20
                else:
                    new_score -= 1
                
                # Lưu trạng thái cũ và cập nhật
                old_val = new_state[nr][nc]
                new_state[nr][nc] = EMPTY
                
                # Nếu không có ma gần, bỏ qua phân tích ma
                if not relevant_ghosts:
                    eval_result = minimax(new_state, (nr, nc), depth_left - 1, new_score, alpha, beta, True, 0, path_length + 1)
                else:
                    eval_result = minimax(new_state, (nr, nc), depth_left, new_score, alpha, beta, False, 0, path_length + 1)
                
                # Khôi phục trạng thái
                new_state[nr][nc] = old_val
                
                # Cập nhật alpha
                max_eval = max(max_eval, eval_result)
                alpha = max(alpha, eval_result)
                
                # Cắt tỉa Alpha-Beta
                if beta <= alpha:
                    break
            
            visited_positions.remove(position_key)
            return max_eval
            
        else:  # Lượt của ma
            relevant_ghosts = get_relevant_ghosts(state, pac_pos)
            
            # Nếu không có ma liên quan
            if ghost_index >= len(relevant_ghosts):
                return minimax(state, pac_pos, depth_left - 1, score, alpha, beta, True, 0, path_length)
            
            min_eval = float("inf")
            g_r, g_c = relevant_ghosts[ghost_index]
            
            # Thử các hướng di chuyển của ma
            for dr, dc in DDX:
                nr, nc = g_r + dr, g_c + dc
                if not isValid2(state, nr, nc, N, M):
                    continue
                
                # Tạo bản sao trạng thái
                new_state = [row[:] for row in state]
                
                # Di chuyển ma
                new_state[g_r][g_c] = EMPTY
                new_state[nr][nc] = MONSTER
                
                # Kiểm tra nếu bắt được Pacman
                if (nr, nc) == pac_pos:
                    eval_result = float("-inf")
                else:
                    # Xử lý ma tiếp theo hoặc trở lại lượt Pacman
                    if ghost_index + 1 < len(relevant_ghosts):
                        eval_result = minimax(new_state, pac_pos, depth_left, score, alpha, beta, False, ghost_index + 1, path_length)
                    else:
                        eval_result = minimax(new_state, pac_pos, depth_left - 1, score, alpha, beta, True, 0, path_length)
                
                # Khôi phục trạng thái
                new_state[g_r][g_c] = MONSTER
                new_state[nr][nc] = EMPTY
                
                # Cập nhật beta
                min_eval = min(min_eval, eval_result)
                beta = min(beta, eval_result)
                
                # Cắt tỉa Alpha-Beta
                if beta <= alpha:
                    break
                    
            return min_eval
    
    # PHẦN CHÍNH: Chiến lược ưu tiên thức ăn an toàn
    
    # Bước 0: Kiểm tra xem có thức ăn ngay lân cận không
    immediate_food = is_immediate_food(_map, pac_row, pac_col)
    if immediate_food:
        return immediate_food
        
    # Bước 1: Tìm thức ăn an toàn
    safe_foods = find_safe_food(_map, pac_row, pac_col, all_ghosts)
    
    # Nếu có thức ăn an toàn, di chuyển đến thức ăn an toàn gần nhất
    if safe_foods:
        _, target_r, target_c = safe_foods[0]
        next_move = find_next_move_to_target(_map, pac_row, pac_col, target_r, target_c, all_ghosts)
        
        # Nếu tìm được nước đi an toàn đến thức ăn an toàn
        if next_move:
            return next_move
    
    # Bước 2: Nếu không có thức ăn an toàn hoặc không tìm được đường đi an toàn, 
    # sử dụng chiến lược AlphaBeta gốc
    
    # Tìm nước đi tốt nhất cho Pacman
    best_score = float("-inf")
    best_move = []
    visited_positions.clear()  # Xóa lịch sử vị trí đã đi
    
    # Lấy ma liên quan
    relevant_ghosts = []
    for r in range(N):
        for c in range(M):
            if _map[r][c] == MONSTER and Manhattan(r, c, pac_row, pac_col) <= 6:
                relevant_ghosts.append((r, c))
    
    # Thử từng hướng di chuyển
    valid_moves = []
    for dr, dc in DDX:
        nr, nc = pac_row + dr, pac_col + dc
        if isValid(_map, nr, nc, N, M):
            # Kiểm tra nước đi an toàn
            safe = is_safe_move(_map, nr, nc, relevant_ghosts)
            valid_moves.append((nr, nc, safe))
    
    # Xếp ưu tiên nước đi an toàn
    valid_moves.sort(key=lambda x: x[2], reverse=True)
    
    for nr, nc, _ in valid_moves:
        # Tạo bản sao trạng thái
        new_state = [row[:] for row in _map]
        
        # Tính điểm mới
        temp_score = Score
        if new_state[nr][nc] == FOOD:
            temp_score += 20
        else:
            temp_score -= 1
        
        # Lưu trạng thái cũ và cập nhật
        old_val = new_state[nr][nc]
        new_state[nr][nc] = EMPTY
        
        # Đánh giá nước đi
        if not relevant_ghosts:
            move_score = minimax(new_state, (nr, nc), MAX_DEPTH, temp_score, float("-inf"), float("inf"), True)
        else:
            move_score = minimax(new_state, (nr, nc), MAX_DEPTH, temp_score, float("-inf"), float("inf"), False)
        
        # Khôi phục trạng thái
        new_state[nr][nc] = old_val
        
        # Cập nhật nước đi tốt nhất
        if move_score > best_score:
            best_score = move_score
            best_move = [nr, nc]
    
    # Nếu không tìm được nước đi tốt, chọn nước đi an toàn đầu tiên
    if not best_move and valid_moves:
        for nr, nc, safe in valid_moves:
            if safe:
                best_move = [nr, nc]
                break
    
    # Nếu vẫn không có, chọn nước đi đầu tiên
    if not best_move and valid_moves:
        best_move = [valid_moves[0][0], valid_moves[0][1]]
    
    return best_move