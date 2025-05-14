import os
import copy
from Algorithms.QLearning import QLearning, save_q_table, load_q_table
from constants import FOOD
from Utils.utils import isValid2

def train_on_map(map_path, episodes=10000):
    with open(map_path, "r") as f:
        N, M = map(int, f.readline().split())
        _map = []
        food_positions = []
        # Lưu map và lưu vị trí FOOD
        for i in range(N):
            line = list(map(int, f.readline().split()))
            for j, cell in enumerate(line):
                if cell == FOOD:
                    food_positions.append([i, j])
            _map.append(line)
        # Lưu vị trí bắt đầu của Pacman
        start_row, start_col = map(int, f.readline().split())

    # Huấn luyện qua các tập episode
    for ep in range(episodes):
        map_copy = copy.deepcopy(_map)
        food = copy.deepcopy(food_positions)
        row, col = start_row, start_col
        steps = 0
        while len(food) > 0 and steps < 300:
            # Gọi hàm QLearning để chọn hành động và cập nhật Q-table
            next_pos = QLearning(map_copy, food, row, col, N, M)
            if not next_pos:
                break
            # Cập nhật vị trí Pacman và tăng số bước
            row, col = next_pos
            steps += 1
        if (ep + 1) % 100 == 0:
            print(f"📘 {os.path.basename(map_path)} - Episode {ep+1}/{episodes} finished")

if __name__ == "__main__":
    level1_folder = "../Input/Level1"
    map_files = [f for f in os.listdir(level1_folder) if f.endswith(".txt")]
    map_files.sort()  # để train theo thứ tự map1 → map2 → ...

    load_q_table()  #  giữ lại các map đã train trước

    for map_file in map_files:
        map_path = os.path.join(level1_folder, map_file)
        print(f"🚀 Training on: {map_file}")
        train_on_map(map_path, episodes=10000)

    save_q_table()
    print("Đã train tất cả map Level1 và lưu qtable.pkl")