from Utils.utils import DDX, isValid2
from constants import FOOD
import random
import pickle # Dùng để lưu và tải Q-table

q_table = {}  # Q-table lưu giá trị Q(s,a)
alpha = 0.2   # Tốc độ học
gamma = 0.95  # Hệ số giảm
epsilon = 0.2 # Tỉ lệ khám phá (exploration rate)

# Chuyển thông tin vị trí Pacman và food thành một tuple để làm state
def encode_state(row, col, food_pos):
    food_tuple = tuple(sorted([tuple(p) for p in food_pos]))
    return (row, col, food_tuple)

# Hàm chọn một hành động dựa trên trạng thái hiện tại 
def choose_action(state):
    if state not in q_table:
        q_table[state] = [0.0 for _ in range(4)]
    if random.random() < epsilon:
        return random.randint(0, 3)
    return q_table[state].index(max(q_table[state]))

# Cập nhật giá trị Q trong Q-table
def update_q(state, action, reward, next_state):
    if state not in q_table:
        q_table[state] = [0.0 for _ in range(4)]
    if next_state not in q_table:
        q_table[next_state] = [0.0 for _ in range(4)]
    predict = q_table[state][action]
    target = reward + gamma * max(q_table[next_state])
    q_table[state][action] += alpha * (target - predict)

def save_q_table(filename="qtable.pkl"):
    with open(filename, "wb") as f:
        pickle.dump(q_table, f)

def load_q_table(filename="qtable.pkl"):
    global q_table
    try:
        with open(filename, "rb") as f:
            q_table = pickle.load(f)
    except FileNotFoundError:
        q_table = {}

def QLearning(_map, _food_Position, row, col, N, M):
    if len(_food_Position) == 0:
        return []

    if len(q_table) == 0:
        load_q_table()

    steps = 0  # số bước hợp lệ (di chuyển)
    expansions = 0  # số hành động Q-Learning thực hiện
    path = [[row, col]]
    current_row, current_col = row, col
    food = _food_Position.copy()

    while len(food) > 0:
        expansions += 1
        state = encode_state(current_row, current_col, food)
        action = choose_action(state)

        d_r, d_c = DDX[action]
        new_row, new_col = current_row + d_r, current_col + d_c

        if not isValid2(_map, new_row, new_col, N, M):
            reward = -10
            new_row, new_col = current_row, current_col
        else:
            reward = -0.5

        if [new_row, new_col] in food:
            reward += 50
            food.remove([new_row, new_col])

        next_state = encode_state(new_row, new_col, food)
        update_q(state, action, reward, next_state)

        # Chỉ tăng step khi có di chuyển thật
        if [new_row, new_col] != [current_row, current_col]:
            path.append([new_row, new_col])
            steps += 1

        current_row, current_col = new_row, new_col

    print(f"✅ Q-Learning: Path found with {steps} steps, {expansions} nodes expanded")
    return path[1:]  # bỏ vị trí ban đầu

