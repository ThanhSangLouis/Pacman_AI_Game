import pygame

from constants import SIZE_WALL, MARGIN

class Wall:
    def __init__(self, row, col, color=None):
        # Định nghĩa màu cam với nhiều sắc thái khác nhau
        self.orange_dark = (200, 80, 0)
        self.orange_medium = (230, 120, 30)  
        self.orange_light = (255, 160, 80)
        self.orange_lighter = (255, 200, 150)
        
        self.image = pygame.Surface([SIZE_WALL, SIZE_WALL], pygame.SRCALPHA)
        
        # Tạo hiệu ứng 3D cho tường
        # Nền cam chính
        pygame.draw.rect(self.image, self.orange_medium, (0, 0, SIZE_WALL, SIZE_WALL))
        
        # Viền sáng bên trái và trên để tạo hiệu ứng 3D
        pygame.draw.line(self.image, self.orange_light, (0, 0), (SIZE_WALL-1, 0), 2)
        pygame.draw.line(self.image, self.orange_light, (0, 0), (0, SIZE_WALL-1), 2)
        
        # Viền tối bên phải và dưới để tạo bóng đổ
        pygame.draw.line(self.image, self.orange_dark, (SIZE_WALL-1, 0), (SIZE_WALL-1, SIZE_WALL-1), 2)
        pygame.draw.line(self.image, self.orange_dark, (0, SIZE_WALL-1), (SIZE_WALL-1, SIZE_WALL-1), 2)
        
        # Tạo chi tiết gạch
        # Đường ngang cho gạch
        num_bricks_horizontal = 2
        brick_height = SIZE_WALL // num_bricks_horizontal
        for i in range(1, num_bricks_horizontal):
            y = i * brick_height
            pygame.draw.line(self.image, self.orange_dark, (0, y), (SIZE_WALL, y), 1)
            
        # Đường dọc cho gạch (xen kẽ giữa các hàng)
        num_bricks_vertical = 3
        brick_width = SIZE_WALL // num_bricks_vertical
        for i in range(1, num_bricks_vertical):
            x = i * brick_width
            # Hàng trên
            pygame.draw.line(self.image, self.orange_dark, (x, 0), (x, brick_height), 1)
            # Hàng dưới 
            if num_bricks_horizontal > 1:
                x_offset = brick_width // 2
                x_shifted = (x + x_offset) % SIZE_WALL
                pygame.draw.line(self.image, self.orange_dark, (x_shifted, brick_height), (x_shifted, SIZE_WALL), 1)
        
        # Tạo texture nhẹ
        for i in range(SIZE_WALL):
            for j in range(SIZE_WALL):
                if (i + j) % 4 == 0:  # Tạo mẫu chấm nhỏ
                    self.image.set_at((i, j), self.orange_lighter)
        
        self.row = row
        self.col = col

        self.rect = self.image.get_rect()
        self.rect.top = row * SIZE_WALL + MARGIN["TOP"]
        self.rect.left = col * SIZE_WALL + MARGIN["LEFT"]

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))