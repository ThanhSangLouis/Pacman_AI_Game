from Utils.utils import DDX, isValid
from constants import FOOD

MAX_DEPTH = 200  # Giới hạn độ sâu để tránh vô hạn vòng lặp

def simulate_path(start_pos, moves):
    r, c = start_pos # Vị trí bắt đầu = vị trí Pacman
    path = [start_pos] # Danh sách lưu các vị trí đã đi qua
    for move in moves: # Duyệt qua các bước đi
        dr, dc = move # Gọi dr, dc: độ dịch chuyển hàng cột = mỗi bước đi  -> nghĩa là Pacman sẽ đi đến ô (r + dr, c + dc)
        r += dr 
        c += dc 
        path.append((r, c)) # Lưu lại toàn bộ hành trình (từ đầu đến cuối).
    return path


def is_valid_path(_map, path, N, M):
    visited = set() # set: là tập hợp, là một kiểu dữ liệu, xài nó vì nó không cho phép trùng lặp
    for r, c in path:
        if not isValid(_map, r, c, N, M): # Nếu ô không hợp lệ (tức là không nằm trong map) thì trả về False
            return False
        if (r, c) in visited: # Nếu ô đã được thăm thì trả về False
            return False
        visited.add((r, c)) # Nếu ô chưa được thăm thì thêm nó vào tập hợp visited
    return True


def is_goal(_map, pos):
    r, c = pos
    return _map[r][c] == FOOD


def Backtracking(_map, start_pos, N, M):
    result_path = []

    def backtrack(current_moves):
        nonlocal result_path # nonlocal: biến cục bộ nhưng có thể truy cập từ bên ngoài hàm

        if len(current_moves) > MAX_DEPTH: # Sâu quá thì dừng lại
            return False

        path = simulate_path(start_pos, current_moves) # Giả lập đường đi từ vị trí bắt đầu đến vị trí hiện tại
        if not is_valid_path(_map, path, N, M): # Nếu đường đi không hợp lệ thì dừng lại
            return False

        if is_goal(_map, path[-1]): # Nếu ô cuối cùng là thức ăn thì lưu lại đường đi
            result_path = path 
            return True

        for dr, dc in DDX: # Duyệt qua các ô lân cận
            if backtrack(current_moves + [(dr, dc)]): # Gọi đệ quy với đường đi mới đến khi tìm thấy thức ăn thì dừng
                return True

        return False # Nếu không tìm thấy thức ăn thì quay lại bước trước đó 

    backtrack([]) # Gọi đệ quy bắt đầu với danh sách rỗng

    # ✅ Debug: xem kết quả thực tế
    print("✅ Final path returned by Backtracking:", result_path)

    # ⚠ Quan trọng: bỏ bước đầu tiên là vị trí hiện tại của Pacman
    return [[r, c] for r, c in result_path[1:]] if len(result_path) > 1 else [] # Trả về đường đi từ vị trí hiện tại đến thức ăn, bỏ qua bước đầu tiên
