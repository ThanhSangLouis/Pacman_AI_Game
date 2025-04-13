import pygame

from constants import SIZE_WALL, MARGIN


class Wall:
    def __init__(self, row, col, color):
        self.image = pygame.Surface([SIZE_WALL, SIZE_WALL]) # Tạo một bề mặt hình ảnh (pygame.Surface) có kích thước bằng một ô trên bản đồ (SIZE_WALL x SIZE_WALL)
        # self.image.fill(color)
        pygame.draw.rect(self.image, color, (0, 0, SIZE_WALL, SIZE_WALL), 1) # 1: Độ dày của đường viền (nếu là 0, hình chữ nhật sẽ được tô đầy)

        self.row = row
        self.col = col

        self.rect = self.image.get_rect()
        self.rect.top = row * SIZE_WALL + MARGIN["TOP"]   # Vị trí y của tường trên bản đồ (theo hàng), nhân với kích thước ô để chuyển từ tọa độ bản đồ sang tọa độ pixel
        self.rect.left = col * SIZE_WALL + MARGIN["LEFT"] # Vị trí x của tường trên bản đồ (theo cột), nhân với kích thước ô để chuyển từ tọa độ bản đồ sang tọa độ pixel

    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))
