import os

import pygame
import sys

from constants import FPS, WIDTH, HEIGHT, BLUE, BLACK, WALL, FOOD, WHITE, YELLOW, MONSTER, IMAGE_GHOST, \
    IMAGE_PACMAN
from constants import LEVEL_TO_ALGORITHM
from Object.Wall import Wall
from Object.Food import Food 

clock = pygame.time.Clock()
bg = pygame.image.load("images/home_bg1.png")
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))
pygame.init()
font = pygame.font.SysFont('Arial', 40)
my_font = pygame.font.SysFont('Comic Sans MS', 70)

_N = _M = 0
__map = 0
SIZE_WALL = 20

# Custom color scheme
BTN_BLUE = "#63B8FF"       # Deep blue for normal
BTN_HOVER = "#FFCC99"      # Light yellow for hover
BTN_TEXT = "#1C1C1C"      # White text
BTN_BORDER = "#FF4500"     # Red border
BACKGROUND_COLOR = "#1C1C1C"  # Light peach skin color

class Button:
    def __init__(self, x, y, width, height, screen, buttonText="Button", onClickFunction=None):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.onClickFunction = onClickFunction
        self.screen = screen
        self.wasClicked = False

        self.fillColors = {
            'normal': BTN_BLUE,
            'hover': BTN_HOVER,
            'pressed': BTN_HOVER
        }

        self.buttonSurface = pygame.Surface((self.width, self.height))
        self.buttonRect = pygame.Rect(self.x, self.y, self.width, self.height)
        self.buttonSurf = font.render(buttonText, True, pygame.Color(BTN_TEXT))

    def process(self):
        mousePos = pygame.mouse.get_pos()
        self.buttonSurface.fill(self.fillColors['normal'])
        if self.buttonRect.collidepoint(mousePos):
            self.buttonSurface.fill(self.fillColors['hover'])
            if pygame.mouse.get_pressed()[0] and not self.wasClicked:
                self.buttonSurface.fill(self.fillColors['pressed'])
                self.wasClicked = True
                if self.onClickFunction:
                    self.onClickFunction()
            elif not pygame.mouse.get_pressed()[0]:
                self.wasClicked = False

        self.buttonSurface.blit(
            self.buttonSurf,
            [
                self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
                self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
            ]
        )
        pygame.draw.rect(self.buttonSurface, pygame.Color(BTN_BORDER), (0, 0, self.width, self.height), 3)
        self.screen.blit(self.buttonSurface, self.buttonRect)

class Menu:
    def __init__(self, screen):
        self.current_level = 0
        self.clicked = False
        self.map_name = []
        self.current_map = 0
        self.done = False
        self.current_screen = 1
        self.screen = screen
        self.btnStart = Button(WIDTH // 2 - 100 + 5, HEIGHT - 170, 200, 100, screen, "Start", self.myFunction)

        self.btnLevel1 = Button(WIDTH // 2 - 150, HEIGHT // 4 * 0 + 20, 300, 100, screen, "Level 1",
                                self._load_map_level_1)
        self.btnLevel2 = Button(WIDTH // 2 - 150, HEIGHT // 4 * 1 + 20, 300, 100, screen, "Level 2",
                                self._load_map_level_2)
        self.btnLevel3 = Button(WIDTH // 2 - 150, HEIGHT // 4 * 2 + 20, 300, 100, screen, "Level 3",
                                self._load_map_level_3)
        self.btnLevel4 = Button(WIDTH // 2 - 150, HEIGHT // 4 * 3 + 20, 300, 100, screen, "Level 4",
                                self._load_map_level_4)

        self.btnPrev = Button(WIDTH // 2 - 250, HEIGHT // 4 * 3 + 35, 100, 100, screen, "<", self.prevMap)
        self.btnNext = Button(WIDTH // 2 + 150, HEIGHT // 4 * 3 + 35, 100, 100, screen, ">", self.nextMap)
        self.btnPlay = Button(WIDTH // 2 - 75, HEIGHT // 4 * 3 + 35, 150, 100, screen, "PLAY", self.selectMap)

        self.btnBack = Button(40, HEIGHT // 4 * 3 + 35, 150, 100, screen, "BACK", self.myFunction)
        self.selected_algorithm = None
        self.algorithm_buttons = []
        self.hover_algorithm_index = -1  # Track hovered button index

    def load_algorithm_buttons(self):
        self.algorithm_buttons = []
        options = []
        if self.current_level == 1:
            options = ["UCS", "DFS", "BFS", "Beam Search", "Greedy", "Backtracking", "Backtracking_Ver2", "AndOr", "Q-Learning"]
        elif self.current_level == 2:
            options = ["UCS", "DFS", "BFS", "Beam Search", "Greedy", "A* Search"]
        elif self.current_level == 3:
            options = ["SimulatedAnnealing", "SA HillClimbing" ]
        elif self.current_level == 4:
            options = ["SimulatedAnnealing", "Minimax", "AlphaBetaPruning"]

        # Tính toán chiều cao tổng cộng của tất cả nút
        button_height = 60
        button_margin = 7  # Khoảng cách giữa các nút
        total_height = len(options) * (button_height + button_margin) - button_margin

        # Vị trí bắt đầu (căn giữa theo chiều dọc)
        start_y = (HEIGHT - total_height) // 2

        # Tạo các nút thuật toán với hiệu ứng
        for idx, algo in enumerate(options):
            btn = AlgorithmButton(
                WIDTH // 2 - 150,  # x
                start_y + idx * (button_height + button_margin),  # y
                300,  # width
                button_height,  # height
                self.screen,
                algo,  # text
                lambda a=algo: self.select_algorithm(a),  # onclick function
                idx  # button index for hover tracking
            )
            self.algorithm_buttons.append(btn)

    def select_algorithm(self, algo_name):
        if self.clicked:
            self.selected_algorithm = algo_name
            
            # Map friendly algorithm names to the exact names expected by SearchAgent
            algorithm_mapping = {
                "BFS": "BFS",
                "DFS": "DFS",
                "A* Search": "A*",
                "Minimax": "Minimax",
                "AlphaBetaPruning": "AlphaBetaPruning",
                "Beam Search": "Beam Search",
                "Greedy": "Greedy",
                "UCS": "UCS",
                "IDA* Search": "IDA*",
                "Backtracking": "Backtracking",
                "Backtracking_Ver2": "Backtracking_ver2",
                "SA HillClimbing": "HillClimbing",
                "AndOr":"AND_OR",
                "Q-Learning": "Q-Learning"
            }
            
            # Use the mapped algorithm name
            if algo_name in algorithm_mapping:
                LEVEL_TO_ALGORITHM[f"LEVEL{self.current_level}"] = algorithm_mapping[algo_name]
            else:
                LEVEL_TO_ALGORITHM[f"LEVEL{self.current_level}"] = algo_name
                
            self.current_screen = 3  # chuyển đến màn chọn map
            # Reset map viewing
            self.current_map = 0
            self.draw_map(self.map_name[self.current_map])
        self.clicked = False

    def nextMap(self):
        if self.clicked:
            self.current_screen = 3
            self.current_map = (self.current_map + 1) % len(self.map_name)
        self.clicked = False

    def prevMap(self):
        if self.clicked:
            self.current_screen = 3
            self.current_map -= 1
            if self.current_map < 0:
                self.current_map += len(self.map_name)
        self.clicked = False

    def myFunction(self):
        self.current_screen = 2
        self.map_name = []
        self.current_map = 0
        self.current_level = 0

    def _load_map_level_1(self):
        if self.clicked:
            self.current_level = 1
            for file in os.listdir('../Input/Level1'):
                self.map_name.append('../Input/Level1/' + file)
            self.current_screen = 5  # CHUYỂN SANG CHỌN THUẬT TOÁN
            self.load_algorithm_buttons()
        self.clicked = False


    # Level 2
    def _load_map_level_2(self):
        if self.clicked:
            self.current_level = 2
            self.map_name = []  # Reset map_name to avoid duplicates
            for file in os.listdir('../Input/Level2'):
                self.map_name.append('../Input/Level2/' + file)
            self.current_screen = 5  # Ensure we set to screen 5 for algorithm selection
            self.load_algorithm_buttons()
        self.clicked = False

    # Level 3
    def _load_map_level_3(self):
        if self.clicked:
            self.current_level = 3
            self.map_name = []  # Reset map_name to avoid duplicates
            for file in os.listdir('../Input/Level3'):
                self.map_name.append('../Input/Level3/' + file)
            self.current_screen = 5  # Ensure we set to screen 5 for algorithm selection
            self.load_algorithm_buttons()
        self.clicked = False


    # Level 4
    def _load_map_level_4(self):
        if self.clicked:
            self.current_level = 4
            for file in os.listdir('../Input/Level4'):
                self.map_name.append('../Input/Level4/' + file)
            self.current_screen = 5  # CHUYỂN SANG CHỌN THUẬT TOÁN
            self.load_algorithm_buttons()
        self.clicked = False


    def draw_map(self, fileName):
        text_surface = my_font.render(
            'LEVEL {level} - MAP {map}'.format(level=self.current_level, map=self.current_map + 1), False, WHITE)
        self.screen.blit(text_surface, (WIDTH // 2 - 270, 0))

        f = open(fileName, "r")
        x = f.readline().split()
        count_ghost = 0
        N, M = int(x[0]), int(x[1])

        MARGIN_TOP = 100
        MARGIN_LEFT = (WIDTH - M * SIZE_WALL) // 2

        for i in range(N):
            line = f.readline().split()
            for j in range(M):
                cell = int(line[j])
                if cell == WALL:
                    top = i * SIZE_WALL + MARGIN_TOP
                    left = j * SIZE_WALL + MARGIN_LEFT
                    wall_preview = Wall(i, j, preview=True)
                    self.screen.blit(wall_preview.image, (left, top))


                elif cell == FOOD:
                    preview_food = Food(i, j, 8, 8, WHITE, preview=True)
                    self.screen.blit(preview_food.image, (j * SIZE_WALL + MARGIN_LEFT, i * SIZE_WALL + MARGIN_TOP))

                elif cell == MONSTER:
                    image = pygame.image.load(IMAGE_GHOST[count_ghost]).convert_alpha()
                    image = pygame.transform.scale(image, (SIZE_WALL, SIZE_WALL))
                    top = i * SIZE_WALL + MARGIN_TOP
                    left = j * SIZE_WALL + MARGIN_LEFT
                    count_ghost = (count_ghost + 1) % len(IMAGE_GHOST)
                    self.screen.blit(image, (left, top))

        x = f.readline().split()
        image = pygame.image.load(IMAGE_PACMAN[0]).convert_alpha()
        image = pygame.transform.scale(image, (SIZE_WALL, SIZE_WALL))
        top = int(x[0]) * SIZE_WALL + MARGIN_TOP
        left = int(x[1]) * SIZE_WALL + MARGIN_LEFT
        self.screen.blit(image, (left, top))

        f.close()

    def selectMap(self):
        if self.clicked:
            self.done = True

    def run(self):
        while not self.done:
            self.clicked = False
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked = True
                if event.type == pygame.MOUSEMOTION:
                    # Update hover state for algorithm buttons
                    mousePos = pygame.mouse.get_pos()
                    if self.current_screen == 5:
                        self.hover_algorithm_index = -1
                        for btn in self.algorithm_buttons:
                            if btn.buttonRect.collidepoint(mousePos):
                                self.hover_algorithm_index = btn.index

            if self.current_screen == 1:
                self.screen.blit(bg, (0, 0))
                self.btnStart.process()

            elif self.current_screen == 2:
                self.screen.fill(pygame.Color(BACKGROUND_COLOR))
                self.btnLevel1.process()
                self.btnLevel2.process()
                self.btnLevel3.process()
                self.btnLevel4.process()

            elif self.current_screen == 3:
                self.screen.fill(pygame.Color(BACKGROUND_COLOR))
                self.current_screen = 4
                self.draw_map(self.map_name[self.current_map])

            elif self.current_screen == 4:
                self.btnNext.process()
                self.btnPrev.process()
                self.btnPlay.process()
                self.btnBack.process()
            elif self.current_screen == 5:
                self.screen.fill(pygame.Color(BACKGROUND_COLOR))
                
                # Draw title
                title_text = f"Select Algorithm for Level {self.current_level}"
                title_surface = pygame.font.SysFont('Arial', 36).render(title_text, True, WHITE)
                self.screen.blit(title_surface, (20, 20)) 
                
                # Draw algorithm buttons with animations
                for btn in self.algorithm_buttons:
                    btn.process(self.hover_algorithm_index)
                
                # Draw back button
                back_btn = Button(40, HEIGHT - 100, 150, 60, self.screen, "Back", self.myFunction)
                back_btn.process()

            pygame.display.flip()
            clock.tick(FPS)

        return [self.current_level, self.map_name[self.current_map]]
class AlgorithmButton(Button):
    def __init__(self, x, y, width, height, screen, buttonText="Button", onClickFunction=None, index=0):
        super().__init__(x, y, width, height, screen, buttonText, onClickFunction)
        self.index = index
        self.animation_offset = 0
        self.animation_direction = 1
        self.animation_speed = 0.15
        self.max_animation = 1.5
        self.fillColors = {
            'normal': BTN_BLUE,
            'hover': BTN_HOVER,
            'pressed': BTN_HOVER
        }
        self.borderColors = {
            'normal': BTN_BORDER,
            'hover': BTN_BORDER,
            'pressed': BTN_BORDER
        }
        self.buttonSurf = font.render(buttonText, True, pygame.Color(BTN_TEXT))

    def process(self, hover_index=-1):
        mousePos = pygame.mouse.get_pos()
        isHovered = self.index == hover_index or self.buttonRect.collidepoint(mousePos)
        if isHovered:
            self.animation_offset += self.animation_speed * self.animation_direction
            if abs(self.animation_offset) >= self.max_animation:
                self.animation_direction *= -1
        else:
            self.animation_offset *= 0.9
        if pygame.mouse.get_pressed()[0] and isHovered and not self.wasClicked:
            self.buttonSurface.fill(self.fillColors['pressed'])
            border_color = pygame.Color(self.borderColors['pressed'])
            self.wasClicked = True
            if self.onClickFunction:
                self.onClickFunction()
        elif isHovered:
            self.buttonSurface.fill(self.fillColors['hover'])
            border_color = pygame.Color(self.borderColors['hover'])
        else:
            self.buttonSurface.fill(self.fillColors['normal'])
            border_color = pygame.Color(self.borderColors['normal'])
        if not pygame.mouse.get_pressed()[0]:
            self.wasClicked = False
        adjusted_x = self.x + (self.animation_offset if isHovered else 0)
        adjusted_y = self.y
        self.buttonSurface.blit(
            self.buttonSurf,
            [
                self.buttonRect.width / 2 - self.buttonSurf.get_rect().width / 2,
                self.buttonRect.height / 2 - self.buttonSurf.get_rect().height / 2
            ]
        )
        pygame.draw.rect(self.buttonSurface, border_color, (0, 0, self.width, self.height), 3)
        self.screen.blit(self.buttonSurface, (adjusted_x, adjusted_y))


