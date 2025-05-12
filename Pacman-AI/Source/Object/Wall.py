import pygame
from constants import SIZE_WALL, MARGIN

class Wall:
    def __init__(self, row, col, color=None, preview=False):
        # Tạo ảnh tường đầy đủ
        full_image = self.build_wall_image()

        # Nếu là preview thì thu nhỏ lại
        if preview:
            self.image = pygame.transform.scale(full_image, (SIZE_WALL // 2, SIZE_WALL // 2))
        else:
            self.image = full_image

        self.row = row
        self.col = col
        self.rect = self.image.get_rect()
        self.rect.top = row * SIZE_WALL + MARGIN["TOP"]
        self.rect.left = col * SIZE_WALL + MARGIN["LEFT"]

    def build_wall_image(self):
        orange_dark = (200, 80, 0)
        orange_medium = (230, 120, 30)
        orange_light = (255, 160, 80)
        orange_lighter = (255, 200, 150)

        image = pygame.Surface([SIZE_WALL, SIZE_WALL], pygame.SRCALPHA)
        pygame.draw.rect(image, orange_medium, (0, 0, SIZE_WALL, SIZE_WALL))

        # Viền sáng trái và trên
        pygame.draw.line(image, orange_light, (0, 0), (SIZE_WALL-1, 0), 2)
        pygame.draw.line(image, orange_light, (0, 0), (0, SIZE_WALL-1), 2)

        # Viền tối phải và dưới
        pygame.draw.line(image, orange_dark, (SIZE_WALL-1, 0), (SIZE_WALL-1, SIZE_WALL-1), 2)
        pygame.draw.line(image, orange_dark, (0, SIZE_WALL-1), (SIZE_WALL-1, SIZE_WALL-1), 2)

        # Gạch ngang
        num_bricks_horizontal = 2
        brick_height = SIZE_WALL // num_bricks_horizontal
        for i in range(1, num_bricks_horizontal):
            y = i * brick_height
            pygame.draw.line(image, orange_dark, (0, y), (SIZE_WALL, y), 1)

        # Gạch dọc xen kẽ
        num_bricks_vertical = 3
        brick_width = SIZE_WALL // num_bricks_vertical
        for i in range(1, num_bricks_vertical):
            x = i * brick_width
            pygame.draw.line(image, orange_dark, (x, 0), (x, brick_height), 1)
            if num_bricks_horizontal > 1:
                x_offset = brick_width // 2
                x_shifted = (x + x_offset) % SIZE_WALL
                pygame.draw.line(image, orange_dark, (x_shifted, brick_height), (x_shifted, SIZE_WALL), 1)

        # Chấm texture
        for i in range(SIZE_WALL):
            for j in range(SIZE_WALL):
                if (i + j) % 4 == 0:
                    image.set_at((i, j), orange_lighter)

        return image

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))
