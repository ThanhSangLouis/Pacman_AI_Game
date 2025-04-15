from Utils.utils import DDX, isValid, Manhattan
from constants import FOOD

def Greedy(_map, food_pos, row, col, N, M):
    """
    Thuật toán Greedy cải tiến với khả năng tìm đường tốt hơn
    """
    # Kiểm tra nếu không còn thức ăn
    if not food_pos or len(food_pos) == 0:
        return []
    
    # Tìm thức ăn gần nhất
    target_food = None
    best_distance = float('inf')
    for food in food_pos:
        dist = Manhattan(row, col, food[0], food[1])
        if dist < best_distance:
            best_distance = dist
            target_food = food
    
    # Nếu Pacman đã ở vị trí thức ăn, trả về vị trí hiện tại
    if [row, col] == target_food:
        return [row, col]

    # Thực hiện tìm kiếm BFS giới hạn để tìm đường đi tốt nhất
    queue = [(row, col, [])]  # (hàng, cột, đường_đi)
    visited = set([(row, col)])
    depth_limit = 10  # Giới hạn độ sâu tìm kiếm
    
    while queue:
        current_row, current_col, path = queue.pop(0)
        
        # Nếu tìm thấy thức ăn, trả về bước đi đầu tiên
        if [current_row, current_col] == target_food:
            if path:
                return path[0]
            return [current_row, current_col]
        
        # Nếu đạt đến giới hạn độ sâu, bỏ qua
        if len(path) >= depth_limit:
            continue
        
        # Đánh giá tất cả các hướng đi có thể
        next_moves = []
        for [d_r, d_c] in DDX:
            new_r, new_c = current_row + d_r, current_col + d_c
            if isValid(_map, new_r, new_c, N, M) and (new_r, new_c) not in visited:
                # Tính khoảng cách đến thức ăn mục tiêu
                dist = Manhattan(new_r, new_c, target_food[0], target_food[1])
                next_moves.append((dist, new_r, new_c))
        
        # Sắp xếp các bước đi theo khoảng cách tăng dần
        next_moves.sort()
        
        # Thêm các bước đi vào hàng đợi
        for _, new_r, new_c in next_moves:
            visited.add((new_r, new_c))
            new_path = path + [[new_r, new_c]] if path else [[new_r, new_c]]
            queue.append((new_r, new_c, new_path))
    
    # Nếu BFS không tìm thấy đường đi, sử dụng phương pháp tham lam đơn giản
    best_move = None
    best_dist = float('inf')
    for [d_r, d_c] in DDX:
        new_r, new_c = row + d_r, col + d_c
        if isValid(_map, new_r, new_c, N, M):
            dist = Manhattan(new_r, new_c, target_food[0], target_food[1])
            if dist < best_dist:
                best_dist = dist
                best_move = [new_r, new_c]
    
    return best_move if best_move else []