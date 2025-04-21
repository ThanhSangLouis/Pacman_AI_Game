from queue import PriorityQueue # Hàng đợi ưu tiên để luôn xử lý trạng thái có chi phí thấp nhất trước
from Utils.utils import isValid, DDX, Manhattan # Manhattan là hàm tính khoảng cách giữa hai điểm

def Greedy(_map, food_pos, row, col, N, M):
    if not food_pos: # Nếu không còn thức ăn nào, trả về danh sách rỗng
        return []

    # Tìm thức ăn gần nhất dựa trên khoảng cách Manhattan
    min_h = float('inf') # Lưu khoảng cách nhỏ nhất
    goal = None # Lưu vị trí thức ăn gần nhất
    for food in food_pos:
        h = Manhattan(row, col, food[0], food[1])
        if h < min_h:
            min_h = h
            goal = food

    # Nếu không tìm thấy thức ăn nào, trả về danh sách rỗng
    if not goal:
        return []

    visited = [[False for _ in range(M)] for _ in range(N)] # Ma trận đánh dấu các ô đã được thăm
    trace = {} # Lưu vết để truy ngược đường đi từ vị trí hiện tại về vị trí bắt đầu

    # Khởi tạo hàng đợi ưu tiên với trạng thái ban đầu (vị trí hiện tại của Pacman)
    q = PriorityQueue()
    q.put((Manhattan(row, col, goal[0], goal[1]), (row, col))) # Đưa vào hàng đợi ưu tiên với giá trị ưu tiên và vị trí hiện tại
    visited[row][col] = True

    # Lặp qua các trạng thái trong hàng đợi ưu tiên
    while not q.empty():
        _, (r, c) = q.get() # Lấy trạng thái có chi phí thấp nhất ra khỏi hàng đợi
        # Nếu đã đến vị trí thức ăn, truy ngược lại đường đi và trả về
        if [r, c] == goal:
            # Bắt đầu từ vị trí mục tiêu, sử dụng trace để tìm vị trí trước đó -> thêm vào path - lặp lại đến vị trí bắt đầu
            path = [[r, c]] 
            while (r, c) != (row, col):
                r, c = trace[(r, c)]
                path.insert(0, [r, c])
            return path

        # Nếu chưa chưa đạt thì duyệt tiếp các ô lân cận
        for d_r, d_c in DDX:
            new_r, new_c = r + d_r, c + d_c
            if isValid(_map, new_r, new_c, N, M) and not visited[new_r][new_c]:
                visited[new_r][new_c] = True
                trace[(new_r, new_c)] = (r, c) # Lưu vết Pacman đã di chuyển đến ô new từ ô (r, c)
                h = Manhattan(new_r, new_c, goal[0], goal[1])
                q.put((h, (new_r, new_c)))
    return []  # Không tìm thấy đường
