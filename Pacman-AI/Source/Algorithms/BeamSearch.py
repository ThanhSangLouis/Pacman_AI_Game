from Utils.utils import isValid, DDX, Manhattan

def BeamSearch(_map, food_pos, row, col, N, M, beam_width=500): # beam_width là số lượng trạng thái tối đa tốt nhất được giữ lại trong mỗi bước
    if not food_pos:
        return []
    # Chọn vị trí thức ăn gần nhất dựa trên khoảng cách Manhattan từ vị trí hiện tại đên vị trí thức ăn
    goal = min(food_pos, key=lambda f: Manhattan(row, col, f[0], f[1]))
    
    state_best_cost = {}  # Dictionary lưu chi phí tốt nhất cho mỗi trạng thái
    beam = [([row, col], [[row, col]], 0)] # Danh sách các trạng thái hiện tại, mỗi trạng thái là một tuple (vị trí, đường đi, chi phí)

    max_iterations = N * M * 4
    iterations = 0
    
    while beam and iterations < max_iterations:
        iterations += 1
        candidates = [] # Danh sách các trạng thái tìm năng trong bước tiếp theo
        
        # Duyệt qua từng trạng thái trong beam -> (r,c): vị trí hiện tại, path: đường đi từ vị trí bắt đầu đến vị trí hiện tại, cost: chi phí
        for (r, c), path, cost in beam:
            if [r, c] == goal:
                return path
            
            # Duyệt qua các ô lân cận
            for d_r, d_c in DDX:
                new_r, new_c = r + d_r, c + d_c
                
                if isValid(_map, new_r, new_c, N, M):
                    new_cost = len(path) + Manhattan(new_r, new_c, goal[0], goal[1]) # Tính chi phí mới là độ dài từ vị trí ban đầu đến ô hiện tại + khoảng cách từ ô mới đến vị trí mục tiêu
            
                    state_key = (new_r, new_c)
                    # Kiểm tra xem trạng thái (new_r, new_c) đã được xử lý trước đó với chi phí tốt hơn hoặc bằng new_cost hay chưa
                    if state_key in state_best_cost and state_best_cost[state_key] <= new_cost:
                        continue
                    
                    # Kiểm tra xem trạng thái (new_r, new_c) có tạo ra một vòng lặp ngay lập tức hay không (Pacman đi qua lại giữa hai ô liên tiếp)
                    if len(path) >= 2 and [new_r, new_c] == path[-2]:
                        continue
                    
                    # Cập nhật chi phí tốt nhất cho trạng thái (new_r, new_c) nếu nó chưa tồn tại hoặc chi phí mới tốt hơn
                    state_best_cost[state_key] = new_cost
                    
                    new_path = path + [[new_r, new_c]] # Cập nhật đường đi mới
                    candidates.append(([new_r, new_c], new_path, new_cost)) # Thêm trạng thái mới vào danh sách candidates
        
        if not candidates:
            break
        
        # Sắp xếp danh sách candidates theo chi phí
        candidates.sort(key=lambda x: x[2])
        
        # Chỉ giữ lại beam_width trạng thái tốt nhất (có chi phí thấp nhất) từ danh sách candidates
        beam = candidates[:beam_width]
    
    # Nếu không tìm thấy đường đi đến thức ăn, trả về danh sách rỗng
    return []