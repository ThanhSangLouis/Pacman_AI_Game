from queue import PriorityQueue
from Utils.utils import DDX, isValid, Manhattan, find_nearest_food
from constants import FOOD
import heapq

def BeamSearch(_map, food_pos, row, col, N, M, beam_width=3):
    """
    Cải thiện Beam Search để tìm đường đến thức ăn hiệu quả hơn.
    Sử dụng cả heuristic và lưu vết đường đi.
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
    
    # Tạo hàng đợi ưu tiên và danh sách đã thăm
    queue = []
    heapq.heappush(queue, (best_distance, 0, (row, col), []))  # (f=h+g, g, vị_trí, đường_đi)
    visited = set([(row, col)])
    max_iterations = 1000  # Giới hạn số lần lặp để tránh vòng lặp vô hạn
    iterations = 0
    
    while queue and iterations < max_iterations:
        iterations += 1
        
        # Chọn beam_width trạng thái tốt nhất
        current_beam = []
        for _ in range(min(beam_width, len(queue))):
            if not queue:
                break
            current_beam.append(heapq.heappop(queue))
        
        # Hàng đợi cho beam tiếp theo
        next_queue = []
        
        # Xử lý mỗi trạng thái trong beam hiện tại
        for _, g, (current_row, current_col), path in current_beam:
            # Kiểm tra nếu đã tìm thấy thức ăn
            if [current_row, current_col] in food_pos:
                if path:  # Nếu có đường đi, trả về bước đầu tiên
                    return path[0]
                return [current_row, current_col]  # Nếu đã ở vị trí thức ăn
            
            # Thử mỗi hướng di chuyển có thể
            for [d_r, d_c] in DDX:
                new_r, new_c = current_row + d_r, current_col + d_c
                
                # Kiểm tra di chuyển hợp lệ và chưa thăm
                if isValid(_map, new_r, new_c, N, M) and (new_r, new_c) not in visited:
                    visited.add((new_r, new_c))
                    
                    # Tạo đường đi mới
                    new_path = path.copy() if path else []
                    if not new_path:
                        new_path = [[new_r, new_c]]
                    else:
                        new_path.append([new_r, new_c])
                    
                    # Tính heuristic và thêm vào hàng đợi tiếp theo
                    new_g = g + 1
                    h = Manhattan(new_r, new_c, target_food[0], target_food[1])
                    f = new_g + h
                    heapq.heappush(next_queue, (f, new_g, (new_r, new_c), new_path))
        
        # Cập nhật hàng đợi chính
        queue = next_queue
    
    # Nếu không tìm thấy đường đi, sử dụng chiến lược backup - chọn ô hợp lệ gần nhất với thức ăn
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