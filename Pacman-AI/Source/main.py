import sys
import pygame
import random

from Algorithms.Ghost_Move import Ghost_move_level4
from Algorithms.SearchAgent import SearchAgent
from Object.Food import Food
from Object.Player import Player
from Object.Wall import Wall
from Utils.utils import DDX, isValid2
from constants import *
from Object.Menu import Menu, Button

N = M = Score = _state_PacMan = 0
_map = []
_wall = []
_road = []
_food = []
_ghost = []
_food_Position = []
_ghost_Position = []
_visited = []
PacMan: Player
Level = 1
Map_name = ""

# Initial Pygame --------------------------
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('PacMan')
clock = pygame.time.Clock()

pygame.font.init()
my_font = pygame.font.SysFont('Comic Sans MS', 30)
my_font_2 = pygame.font.SysFont('Comic Sans MS', 100)


# ------------------------------------------

def readMapInFile(map_name: str):
    f = open(map_name, "r")
    x = f.readline().split() # x là danh sách gồm 2 phần tử: số hàng và số cột của bản đồ
    global N, M, _map
    _map = [] # Khởi tạo bản đồ rỗng
    N, M = int(x[0]), int(x[1])
    for _ in range(N): # Lặp lại N lần để đọc từng dòng của bản đồ
        # Mỗi dòng sẽ được tách thành các phần tử và lưu vào danh sách _m (1: Tường 0: Ô trống 2: Thức ăn 3: Ma 9: Pac-Man (nếu có))
        line = f.readline().split()
        _m = []
        for j in range(M): # Lặp lại M lần để đọc từng phần tử trong dòng
            _m.append(int(line[j])) # Thêm phần tử vào danh sách _m
        _map.append(_m) # Thêm danh sách _m vào bản đồ _map

    # Tạo đối tượng Pacman từ lớp Player và tính toán vị trí của nó
    global PacMan
    x = f.readline().split() # Đọc dòng cuối cùng để lấy vị trí của PacMan
    MARGIN["TOP"] = max(0, (HEIGHT - N * SIZE_WALL) // 2) # Tính toán vị trí của PacMan theo chiều dọc
    MARGIN["LEFT"] = max(0, (WIDTH - M * SIZE_WALL) // 2) # Tính toán vị trí của PacMan theo chiều ngang
    PacMan = Player(int(x[0]), int(x[1]), IMAGE_PACMAN[0])

    f.close()


# --------------------------------- MAIN ---------------------

def check_Object(_map, row, col):
    if _map[row][col] == WALL:
        _wall.append(Wall(row, col, BLUE))

    # hidden else later
    else:
        pass
        # _road.append(Food(row, col, BLOCK_SIZE // 3, BLOCK_SIZE // 3, GREEN))

    if _map[row][col] == FOOD:
        _food.append(Food(row, col, BLOCK_SIZE, BLOCK_SIZE, YELLOW))
        _food_Position.append([row, col])

    if _map[row][col] == MONSTER:
        _ghost.append(Player(row, col, IMAGE_GHOST[len(_ghost) % len(IMAGE_GHOST)]))
        _ghost_Position.append([row, col])


def initData() -> None:
    global N, M, _map, _food_Position, _food, _road, _wall, _ghost, _visited, Score, _state_PacMan, _ghost_Position
    N = M = Score = _state_PacMan = 0
    _map = []
    _wall = []
    _road = []
    _food = []
    _ghost = []
    _food_Position = []
    _ghost_Position = []

    readMapInFile(map_name=Map_name)
    _visited = [[0 for _ in range(M)] for _ in range(N)]

    for row in range(N):
        for col in range(M):
            check_Object(_map, row, col)


def Draw(_screen) -> None:
    for wall in _wall:
        wall.draw(_screen)
    for road in _road:
        road.draw(_screen)
    for food in _food:
        food.draw(_screen)
    for ghost in _ghost:
        ghost.draw(_screen)

    PacMan.draw(_screen)

    text_surface = my_font.render('Score: {Score}'.format(Score=Score), False, RED)
    screen.blit(text_surface, (0, 0))


# 1: Random, 2: A*
def generate_Ghost_new_position(_ghost, _type: int = 0) -> list[list[int]]: # Tạo vị trí mới cho ma dựa trên loại thuật toán
    _ghost_new_position = []
    if _type == 1: # Di chuyển ngẫu nhiên
        for idx in range(len(_ghost)): # Duyệt qua từng ma
            [row, col] = _ghost[idx].getRC() # Lấy vị trí hiện tại của ma

            rnd = random.randint(0, 3) # Chọn ngẫu nhiên 1 trong 4 hướng di chuyển (trái, phải, lên, xuống)
            new_row, new_col = row + DDX[rnd][0], col + DDX[rnd][1] # Tính toán vị trí mới của ma DDX[rnd][0] là hàng, DDX[rnd][1] là cột
            while not isValid2(_map, new_row, new_col, N, M): # Kiểm tra xem vị trí mới có hợp lệ không (không phải tường)
                rnd = random.randint(0, 3) # Nếu không hợp lệ thì chọn lại hướng di chuyển ngẫu nhiên
                new_row, new_col = row + DDX[rnd][0], col + DDX[rnd][1]

            _ghost_new_position.append([new_row, new_col]) # Thêm vị trí mới vào danh sách vị trí mới của ma

    # update latest
    elif _type == 2:
        for idx in range(len(_ghost)): # Duyệt qua từng ma
            [start_row, start_col] = _ghost[idx].getRC() # Lấy vị trí hiện tại của ma
            [end_row, end_col] = PacMan.getRC() # Lấy vị trí của PacMan 
            _ghost_new_position.append(Ghost_move_level4(_map, start_row, start_col, end_row, end_col, N, M)) # Tính toán vị trí mới của ma dựa trên thuật toán A* tức là tìm đường đi ngắn nhất từ vị trí hiện tại của ma đến vị trí của PacMan
    #=>> Di chuyển đến vị trí gần nhất với PacMan
    return _ghost_new_position

# Kiểm tra va chạm giữa PacMan và ma
def check_collision_ghost(_ghost, pac_row=-1, pac_col=-1) -> bool:
    Pac_pos = [pac_row, pac_col] # pac_row, pac_col là vị trí của PacMan
    # Nếu pac_row = -1 thì lấy vị trí hiện tại của PacMan
    if pac_row == -1:
        Pac_pos = PacMan.getRC()
    for g in _ghost: # Duyệt qua từng ma
        Ghost_pos = g.getRC() # Lấy vị trí hiện tại của ma
        if Pac_pos == Ghost_pos:
            return True
    return False

# Hàm thay đổi hướng di chuyển (góc quay) của PacMan dựa trên vị trí mới
def change_direction_PacMan(new_row, new_col):
    global PacMan, _state_PacMan # PacMan là đối tượng PacMan, _state_PacMan là trạng thái hiện tại của PacMan
    [current_row, current_col] = PacMan.getRC() # Lấy vị trí hiện tại của PacMan
    _state_PacMan = (_state_PacMan + 1) % len(IMAGE_PACMAN) # Cập nhật trạng thái của PacMan bằng cách lấy phần tử tiếp theo trong danh sách IMAGE_PACMAN

    if new_row > current_row: # Nếu vị trí mới của PacMan nằm dưới vị trí hiện tại thì di chuyển xuống dưới
        PacMan.change_state(-90, IMAGE_PACMAN[_state_PacMan])
    elif new_row < current_row: # Nếu vị trí mới của PacMan nằm trên vị trí hiện tại thì di chuyển lên trên
        PacMan.change_state(90, IMAGE_PACMAN[_state_PacMan])
    elif new_col > current_col: # Nếu vị trí mới của PacMan nằm bên phải vị trí hiện tại thì di chuyển sang phải
        PacMan.change_state(0, IMAGE_PACMAN[_state_PacMan])
    elif new_col < current_col:
        PacMan.change_state(180, IMAGE_PACMAN[_state_PacMan]) # Nếu vị trí mới của PacMan nằm bên trái vị trí hiện tại thì di chuyển sang trái

# Hàm kiểm tra xem vị trí mới có hợp lệ không (không phải tường)
def randomPacManNewPos(_map, row, col, _N, _M):
    for [d_r, d_c] in DDX: # Duyệt qua từng hướng di chuyển (trái, phải, lên, xuống)
        new_r, new_c = d_r + row, d_c + col # Tính toán vị trí mới của PacMan bằng cách cộng thêm hướng di chuyển vào vị trí hiện tại
        if isValid2(_map, new_r, new_c, _N, _M): # Kiểm tra xem vị trí mới có hợp lệ không (không phải tường)
            return [new_r, new_c]


def startGame() -> None: 
    global _map, _visited, Score # visited: lưu số lần Pac-Man đi qua mỗi ô (dùng trong Local Search)
    _ghost_new_position = []
    result = []
    new_PacMan_Pos: list = []
    initData() # Đọc dữ liệu bản đồ, khởi tạo Pac-Man, ma, thức ăn
    pac_can_move = True

    done = False
    is_moving = False
    timer = 0

    status = 0
    delay = 100

    # ----------------- Run pygame
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                showMenu()
                return
        
        if delay > 0:  # Dùng để tạo độ trễ giữa các bước di chuyển → giúp game mượt hơn
            delay -= 1
        # handle move step by step
        if delay <= 0:
            if is_moving:
                timer += 1
                # Ghost move
                if len(_ghost_new_position) > 0: # Nếu có vị trí mới cho ma thì di chuyển
                    for idx in range(len(_ghost)): # Duyệt qua từng ma
                        [old_row_Gho, old_col_Gho] = _ghost[idx].getRC() # Lấy vị trí hiện tại của ma
                        [new_row_Gho, new_col_Gho] = _ghost_new_position[idx] # Lấy vị trí mới của ma

                        if old_row_Gho < new_row_Gho: # di chuyển xuống dưới
                            _ghost[idx].move(1, 0)
                        elif old_row_Gho > new_row_Gho: # di chuyển lên trên
                            _ghost[idx].move(-1, 0)
                        elif old_col_Gho < new_col_Gho: # di chuyển sang phải
                            _ghost[idx].move(0, 1)
                        elif old_col_Gho > new_col_Gho: 
                            _ghost[idx].move(0, -1) # di chuyển sang trái

                        if timer >= SIZE_WALL: # Nếu timer lớn hơn SIZE_WALL thì ma sẽ dừng lại và cập nhật vị trí mới
                            _ghost[idx].setRC(new_row_Gho, new_col_Gho) # Cập nhật vị trí mới của ma

                            _map[old_row_Gho][old_col_Gho] = EMPTY # Cập nhật ô cũ của ma thành ô trống
                            _map[new_row_Gho][new_col_Gho] = MONSTER # Cập nhật ô mới của ma thành ô ma

                            # check touch Food
                            # Nếu trước đó là ô thức ăn, thì sau khi ma đi qua sẽ phục hồi lại ô thức ăn.
                            for index in range(len(_food)):
                                [row_food, col_food] = _food[index].getRC()
                                if row_food == old_row_Gho and col_food == old_col_Gho:
                                    _map[row_food][col_food] = FOOD

                # Pacman move
                if len(new_PacMan_Pos) > 0:
                    [old_row_Pac, old_col_Pac] = PacMan.getRC()
                    
                    # Fix for the "too many values to unpack" error
                    # Ensure we only take the first two elements from new_PacMan_Pos
                    if isinstance(new_PacMan_Pos, list):
                        if len(new_PacMan_Pos) >= 2:
                            # If new_PacMan_Pos is longer than 2 items, take only the first two
                            new_row_Pac, new_col_Pac = new_PacMan_Pos[0], new_PacMan_Pos[1]
                        else:
                            # Handle case where new_PacMan_Pos is a list with nested lists
                            if isinstance(new_PacMan_Pos[0], list) and len(new_PacMan_Pos[0]) >= 2:
                                new_row_Pac, new_col_Pac = new_PacMan_Pos[0][0], new_PacMan_Pos[0][1]
                            else:
                                # Skip this iteration if format is unexpected
                                is_moving = False
                                continue
                    else:
                        # If it's not a list, skip this iteration
                        is_moving = False
                        continue

                    # After extracting the values, make sure they are integers
                    if isinstance(new_row_Pac, list):
                        # Handle nested lists - extract the values properly
                        if len(new_row_Pac) > 1:
                            new_col_Pac = new_row_Pac[1]
                            new_row_Pac = new_row_Pac[0]
                        else:
                            new_row_Pac = new_row_Pac[0]
                    
                    # Now that we have integers, compare and move
                    if isinstance(new_row_Pac, int) and isinstance(new_col_Pac, int):
                        if old_row_Pac < new_row_Pac:
                            PacMan.move(1, 0) # di chuyển xuống dưới
                        elif old_row_Pac > new_row_Pac:
                            PacMan.move(-1, 0) # di chuyển lên trên
                        elif old_col_Pac < new_col_Pac:
                            PacMan.move(0, 1) # di chuyển sang phải
                        elif old_col_Pac > new_col_Pac:
                            PacMan.move(0, -1) # di chuyển sang trái
                    else:
                        # If we couldn't get valid integers, skip this iteration
                        is_moving = False
                        new_PacMan_Pos = []
                        continue
                    
                    # Nếu timer lớn hơn SIZE_WALL thì PacMan sẽ dừng lại và cập nhật vị trí mới
                    # Nếu PacMan chạm vào tường thì sẽ dừng lại và cập nhật vị trí mới
                    if timer >= SIZE_WALL or PacMan.touch_New_RC(new_row_Pac, new_col_Pac):
                        is_moving = False
                        PacMan.setRC(new_row_Pac, new_col_Pac)
                        Score -= 1

                        # check touch Food
                        for idx in range(len(_food)):
                            [row_food, col_food] = _food[idx].getRC()
                            if row_food == new_row_Pac and col_food == new_col_Pac:
                                _map[row_food][col_food] = EMPTY
                                _food.pop(idx) # Xóa thức ăn khỏi danh sách thức ăn
                                _food_Position.pop(idx) # Xóa thức ăn khỏi danh sách vị trí thức ăn
                                Score += 20
                                break # Thoát khỏi vòng lặp nếu đã tìm thấy thức ăn
                        new_PacMan_Pos = []

                if check_collision_ghost(_ghost): # Nếu PacMan chạm vào ma thì dừng lại và cập nhật vị trí mới
                    pac_can_move = False
                    done = True
                    status = -1

                if len(_food_Position) == 0: # Nếu không còn thức ăn thì dừng lại và cập nhật vị trí mới
                    status = 1
                    done = True

                if timer >= SIZE_WALL:# Nếu timer lớn hơn SIZE_WALL thì dừng lại và cập nhật vị trí mới
                    is_moving = False
            else:
                # _type = [0:don't move(default), 1:Random, 2:A*]
                if Level == 3:
                    _ghost_new_position = generate_Ghost_new_position(_ghost, _type=1)
                elif Level == 4:
                    _ghost_new_position = generate_Ghost_new_position(_ghost, _type=2)
                else:
                    _ghost_new_position = generate_Ghost_new_position(_ghost, _type=0)

                is_moving = True
                timer = 0

                if not pac_can_move:
                    continue

                [row, col] = PacMan.getRC()

                # cài đặt thuật toán ở đây, thay đổi ALGORITHM trong file constants.py
                # thuật toán chỉ cần trả về vị trí mới theo format [new_row, new_col] cho biến new_PacMan_Pos
                # VD: new_PacMan_Pos = [4, 5]
                # thuật toán sẽ được cài đặt trong folder Algorithms

                search = SearchAgent(_map, _food_Position, row, col, N, M) # Khởi tạo thuật toán tìm kiếm
                if Level == 1 or Level == 2: # Level 1, 2: tìm kiếm theo chiều rộng (BFS) hoặc chiều sâu (DFS)
                    if len(result) <= 0:     # Nếu chưa tìm thấy đường đi thì tìm kiếm lại
                        result = search.execute(ALGORITHMS=LEVEL_TO_ALGORITHM[f"LEVEL{Level}"])
                        if result is None:  # Nếu thuật toán không trả về kết quả, gán result là danh sách rỗng
                            result = []
                        if len(result) > 0: # Nếu tìm thấy đường đi thì lấy vị trí đầu tiên
                            result.pop(0)   # Bỏ qua vị trí đầu tiên vì đó là vị trí hiện tại của PacMan
                            new_PacMan_Pos = result[0] # Lấy vị trí tiếp theo để di chuyển

                    elif len(result) > 1: # Nếu đã tìm thấy đường đi thì lấy vị trí tiếp theo
                        result.pop(0)
                        new_PacMan_Pos = result[0]

                elif Level == 3 and len(_food_Position) > 0: 
                    # Sử dụng thuật toán người dùng chọn thay vì mặc định
                    if LEVEL_TO_ALGORITHM["LEVEL3"] in ["BFS", "DFS", "A*", "UCS", "Greedy", "Beam Search", "IDA*", "IDS", "AlphaBeta"]:
                        if len(result) <= 0:
                            result = search.execute(ALGORITHMS=LEVEL_TO_ALGORITHM["LEVEL3"])
                            if result is None:
                                result = []
                                new_PacMan_Pos = []
                            elif len(result) > 1:
                                result.pop(0)
                                new_PacMan_Pos = result[0]
                            else:
                                result = []
                                new_PacMan_Pos = []

                        elif len(result) > 1:
                            result.pop(0)
                            new_PacMan_Pos = result[0]
                        else:  # Dù là 1 phần tử cũng không đủ đi tiếp → reset
                            result = []
                            new_PacMan_Pos = []

                    else:
                        # Nếu là Local Search hoặc thuật toán khác thì dùng cách cũ
                        new_PacMan_Pos = search.execute(ALGORITHMS=LEVEL_TO_ALGORITHM["LEVEL3"], visited=_visited)
                        _visited[row][col] += 1  # Cập nhật số lần PacMan đi qua ô này


                elif Level == 4 and len(_food_Position) > 0:
                    new_PacMan_Pos = search.execute(ALGORITHMS=LEVEL_TO_ALGORITHM["LEVEL4"], depth=4, Score=Score)

                if len(_food_Position) > 0 and (not isinstance(new_PacMan_Pos, list) or len(new_PacMan_Pos) == 0 or [row, col] == new_PacMan_Pos): # Nếu không tìm thấy đường đi thì di chuyển ngẫu nhiên
                    new_PacMan_Pos = randomPacManNewPos(_map, row, col, N, M)
                if len(new_PacMan_Pos) > 0: # Nếu tìm thấy đường đi thì di chuyển
                    # Check if new_PacMan_Pos[0] is a list or an integer
                    if isinstance(new_PacMan_Pos[0], list):
                        # If it's a list, extract the row and column
                        change_direction_PacMan(new_PacMan_Pos[0][0], new_PacMan_Pos[0][1])
                        if check_collision_ghost(_ghost, new_PacMan_Pos[0][0], new_PacMan_Pos[0][1]):
                            pac_can_move = False
                            done = True
                            status = -1
                    else:
                        # If it's already integers, proceed as normal
                        change_direction_PacMan(new_PacMan_Pos[0], new_PacMan_Pos[1])
                        if check_collision_ghost(_ghost, new_PacMan_Pos[0], new_PacMan_Pos[1]):
                            pac_can_move = False
                            done = True
                            status = -1

        # ------------------------------------------------------

        screen.fill(BLACK)
        Draw(screen)
        pygame.display.flip()
        clock.tick(FPS)

    handleEndGame(status)


done_2 = False

# Hàm hiển thị màn hình kêt thúc game (thắng hoặc thua)
# status = -1: thua, 1: thắng
def handleEndGame(status: int):
    global done_2
    done_2 = False
    bg = pygame.image.load("images/gameover_bg.png")
    bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
    bg_w = pygame.image.load("images/win.jpg")
    bg_w = pygame.transform.scale(bg_w, (WIDTH, HEIGHT))

    def clickContinue():
        global done_2
        done_2 = True

    def clickQuit():
        pygame.quit()
        sys.exit(0)

    btnContinue = Button(WIDTH // 2 - 300, HEIGHT // 2 - 50, 200, 100, screen, "CONTINUE", clickContinue)
    btnQuit = Button(WIDTH // 2 + 50, HEIGHT // 2 - 50, 200, 100, screen, "QUIT", clickQuit)

    delay = 100
    while not done_2:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit(0)

        if delay > 0:
            delay -= 1
            pygame.display.flip()
            clock.tick(FPS)
            continue

        if status == -1:
            screen.blit(bg, (0, 0))
        else:
            screen.blit(bg_w, (0, 0))
            text_surface = my_font_2.render('Your Score: {Score}'.format(Score=Score), False, RED)
            screen.blit(text_surface, (WIDTH // 4 - 65, 10))

        btnQuit.process()
        btnContinue.process()

        pygame.display.flip()
        clock.tick(FPS)

    showMenu()


def showMenu():
    _menu = Menu(screen) # Hiển thị menu
    global Level, Map_name
    [Level, Map_name] = _menu.run() # Lấy level và bản đồ đã chọn
    startGame()


if __name__ == '__main__':
    showMenu()
    pygame.quit()
