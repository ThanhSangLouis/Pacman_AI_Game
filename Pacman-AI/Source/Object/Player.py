import pygame

from constants import SIZE_WALL, MARGIN
# SIZE WALL: Kích thước của một ô trên bản đồ
# MARGIN: Lề trên và lề trái của bản đồ, dùng để căn chỉnh vị trí của các đối tượng trên màn hình
class Player:
    def __init__(self, row, col, fileImage):
        self.image = pygame.image.load(fileImage).convert_alpha()
        self.image = pygame.transform.scale(self.image, (SIZE_WALL, SIZE_WALL)) # Thay đổi kích thước hình ảnh để phù hợp với kích thước ô

        self.rect = self.image.get_rect() # Lấy hình chữ nhật bao quanh hình ảnh
        self.rect.top = row * SIZE_WALL + MARGIN["TOP"]
        self.rect.left = col * SIZE_WALL + MARGIN["LEFT"]
        self.row = row
        self.col = col

    # Hàm thay đổi trạng thái của đối tượng (hình ảnh và góc quay)
    def change_state(self, rotate, fileImage):
        self.image = pygame.image.load(fileImage).convert_alpha()
        self.image = pygame.transform.scale(self.image, (SIZE_WALL, SIZE_WALL))
        self.image = pygame.transform.rotate(self.image, rotate)

        # Cập nhật lại vị trí của hình chữ nhật (self.rect) để đảm bảo hình ảnh mới được căn chỉnh đúng vị trí trên màn hình
        self.rect = self.image.get_rect()
        self.rect.top = self.row * SIZE_WALL + MARGIN["TOP"]
        self.rect.left = self.col * SIZE_WALL + MARGIN["LEFT"]

    
    def draw(self, screen):
        screen.blit(self.image, (self.rect.left, self.rect.top))

    # Lấy vị trí hàng (row) và cột (col) của đối tượng trên bản đồ
    def getRC(self):
        return [self.row, self.col]

    #  Cập nhật vị trí hàng (row) và cột (col) của đối tượng trên bản đồ
    def setRC(self, row, col):
        self.row = row
        self.col = col
        self.rect.top = row * SIZE_WALL + MARGIN["TOP"]
        self.rect.left = col * SIZE_WALL + MARGIN["LEFT"]


    # Di chuyển đối tượng theo hướng đã cho (d_R: di chuyển theo hàng, d_C: di chuyển theo cột)
    def move(self, d_R, d_C):
        self.rect.top += d_R
        self.rect.left += d_C

    #  Kiểm tra xem đối tượng đã đến vị trí mới trên màn hình hay chưa
    def touch_New_RC(self, row, col):
        return self.rect.top == row * SIZE_WALL and self.rect.left == col * SIZE_WALL