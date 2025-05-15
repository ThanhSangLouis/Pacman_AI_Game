def BFS(_map, start_row, start_col, goal_row, goal_col, N, M):
    """
    Thuật toán BFS thuần tìm đường đi từ điểm bắt đầu (start_row, start_col)
    đến điểm đích (goal_row, goal_col) trên một ma trận.

    Parameters:
    - _map: Ma trận biểu diễn bản đồ.
    - start_row, start_col: Tọa độ điểm bắt đầu.
    - goal_row, goal_col: Tọa độ điểm đích.
    - N, M: Kích thước của ma trận (số hàng và số cột).

    Returns:
    - path: Danh sách các ô trên đường đi từ điểm bắt đầu đến điểm đích.
    """
    # Tạo mảng visited (đã thăm) và trace (dấu vết) để theo dõi đường đi
    visited = [[False for _ in range(M)] for _ in range(N)]
    trace = [[[-1, -1] for _ in range(M)] for _ in range(N)]

    # Khởi tạo hàng đợi BFS
    queue = [(start_row, start_col)]
    visited[start_row][start_col] = True

    # Định nghĩa các hướng di chuyển (lên, xuống, trái, phải)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Vòng lặp BFS
    while queue:
        row, col = queue.pop(0)

        # Kiểm tra nếu đã tới được ô đích
        if row == goal_row and col == goal_col:
            # Truy vết lại đường đi từ điểm đích về điểm bắt đầu
            path = [[goal_row, goal_col]]
            cur_row, cur_col = goal_row, goal_col
            while True:
                prev_row, prev_col = trace[cur_row][cur_col]
                if prev_row == -1 and prev_col == -1:
                    break
                path.insert(0, [prev_row, prev_col])
                cur_row, cur_col = prev_row, prev_col
            return path

        # Duyệt qua các ô kề
        for d_r, d_c in directions:
            new_row, new_col = row + d_r, col + d_c
            if (0 <= new_row < N and 0 <= new_col < M and  # Kiểm tra trong phạm vi
                _map[new_row][new_col] != 1 and           # Ô không phải là vật cản
                not visited[new_row][new_col]):          # Ô chưa được thăm
                visited[new_row][new_col] = True
                queue.append((new_row, new_col))
                trace[new_row][new_col] = [row, col]

    # Nếu không tìm thấy đường đi, trả về danh sách rỗng
    return []