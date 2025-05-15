from Utils.utils import DDX, isValid # DDX: danh sách các hướng di chuyển
from constants import FOOD
from collections import deque # deque: là một kiểu dữ liệu giống như list nhưng có thể thêm hoặc xóa phần tử từ cả hai đầu
MAX_DEPTH = 200  # Giới hạn độ sâu để tránh vô hạn vòng lặp


def simulate_path(start_pos, moves): # Giả lập đường đi từ vị trí bắt đầu đến vị trí hiện tại
    r, c = start_pos
    path = [start_pos]
    for move in moves:
        dr, dc = move
        r += dr
        c += dc
        path.append((r, c))
    return path


def is_goal(_map, pos): # Kiểm tra xem ô hiện tại có phải là thức ăn không
    r, c = pos
    return _map[r][c] == FOOD


def get_neighbors(pos, _map, N, M): # Lấy danh sách các ô lân cận
    r, c = pos  # Vị trí hiện tại
    neighbors = [] # Tao danh sách lưu các ô lân cận
    
    for dr, dc in DDX: 
        nr, nc = r + dr, c + dc # tính tọa độ ô lân cận mới
        if isValid(_map, nr, nc, N, M): # Nếu ô lân cận hợp lệ thì thêm vào danh sách neighbors
            neighbors.append((nr, nc))
    return neighbors


def ac3(domains, _map, N, M):
    
    queue = deque() # Tạo hàng đợi , deque: là một kiểu dữ liệu giống như list nhưng có thể thêm hoặc xóa phần tử từ cả hai đầu
    
    for var in domains: # Duyệt qua tất cả các ô ở trong domains
        for neighbor in get_neighbors(var, _map, N, M): # Với mỗi biến var (tức mỗi ô hợp lệ trên bản đồ), ta gọi hàm get_neighbors để lấy danh sách tất cả các ô kế bên hợp lệ của var.
            queue.append((var, neighbor)) # Thêm cặp cung (var, neighbor) vào hàng đợi queue.


    while queue:
        xi, xj = queue.popleft() # Lấy cặp cung (xi, xj) ra khỏi hàng đợi
        if revise(domains, xi, xj): # Nếu hàm revise trả về True thì có nghĩa là đã sửa đổi miền của xi
            if not domains[xi]: # Nếu miền của xi rỗng thì không thể tìm được đường đi
                return False
            for xk in get_neighbors(xi, _map, N, M): # Lấy danh sách các ô lân cận của xi
                if xk != xj: # Nếu ô lân cận không phải là xj thì thêm vào hàng đợi
                    queue.append((xk, xi))
    return True


def revise(domains, xi, xj):
    revised = False 
    to_remove = [] # Lưu các giá trị cần xóa
    for x in domains[xi]: # Duyệt qua tất cả các giá trị trong miền của xi
        if not any(True for y in domains[xj] if y != x): # Kiểm tra xem trong miền xj có ít nhất một giá trị y khác x không.
            # Nếu không có giá trị y nào khác x → nghĩa là x không tương thích với bất kỳ giá trị nào trong miền xj
            # Thì x cần bị xóa khỏi miền của xi -> trả về True
            to_remove.append(x) 
            revised = True

    for val in to_remove: # Nếu có giá trị nào cần xóa thì xóa nó khỏi miền của xi
        domains[xi].remove(val)
    return revised # Trả về True nếu đã sửa đổi miền của xi, ngược lại trả về False


def Backtracking_ver2(_map, start_pos, N, M):
    result_path = []
    visited = set()

    # Khởi tạo domain ban đầu cho tất cả ô
    domains = {}

    for r in range(N):
        for c in range(M):
            if isValid(_map, r, c, N, M):
                domains[(r, c)] = DDX.copy()

    # Chạy AC-3 toàn cục trước khi bắt đầu
    if not ac3(domains, _map, N, M):  # Nếu AC-3 trả về False, tức miền biến bị rỗng, không có lời giải → thoát luôn.
        print("❌ AC-3 failed to find arc consistency.")
        return []

    def backtrack(current_moves, current_pos): # Hàm đệ quy để tìm đường đi
        nonlocal result_path # nonlocal: biến cục bộ nhưng có thể truy cập từ bên ngoài hàm

        if len(current_moves) > MAX_DEPTH: # Giới hạn độ sâu để tránh vô hạn vòng lặp
            return False

        r, c = current_pos 
        if (r, c) in visited:  # Nếu đã đi qua ô này rồi, tránh đi lại → quay lui.
            return False

        visited.add((r, c)) # Đánh dấu ô này đã được thăm
 
        if is_goal(_map, current_pos): # Nếu ô hiện tại là thức ăn thì lưu lại đường đi
            result_path = simulate_path(start_pos, current_moves)
            return True

        for dr, dc in domains.get(current_pos, []): # Chỉ thử những bước đi được phép theo miền giá trị đã được AC-3 tối ưu,
            nr, nc = r + dr, c + dc # Tính tọa độ ô lân cận mới
            if isValid(_map, nr, nc, N, M): # Nếu ô lân cận hợp lệ thì thêm vào danh sách neighbors
                if backtrack(current_moves + [(dr, dc)], (nr, nc)): # Gọi đệ quy với đường đi mới đến khi tìm thấy thức ăn thì dừng
                    return True

        visited.remove((r, c)) # Nếu không tìm thấy thức ăn thì quay lại bước trước đó
        return False

    backtrack([], start_pos) # GỌI đệ quy bắt đầu với danh sách rỗng và vị trí bắt đầu

    print("✅ Final path returned by Backtracking + AC-3 (global):", result_path)
    return [[r, c] for r, c in result_path[1:]] if len(result_path) > 1 else []
