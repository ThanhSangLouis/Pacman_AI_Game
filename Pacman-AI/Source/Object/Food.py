import pygame
import math
import random

from constants import WHITE, SIZE_WALL, YELLOW, BLUE_FOOD, MARGIN

class Food:
    def __init__(self, row, col, width, height, color):
        # Giảm kích thước surface để hiệu ứng nhẹ nhàng hơn
        self.image = pygame.Surface([width + 10, height + 10], pygame.SRCALPHA)
        
        # Định nghĩa các màu xanh dương nhẹ nhàng
        self.colors = {
            'blue_bright': (100, 180, 255),  # Xanh dương sáng
            'blue_main': (60, 130, 230),     # Xanh dương chính 
            'blue_deep': (40, 90, 200),      # Xanh dương đậm
            'blue_shadow': (30, 60, 140),    # Bóng xanh
            'glow_blue': (120, 200, 255, 60),# Ánh sáng xanh mờ (giảm alpha)
            'power_blue': (150, 220, 255),   # Xanh cho power pellet
            'power_glow': (180, 240, 255, 70), # Glow cho power pellet
        }
        
        self.base_color = color
        self.center_x = width // 2 + 4
        self.center_y = height // 2 + 4
        
        # Tạo food dựa trên loại
        if color == WHITE:  # Regular blue pellet
            self._create_blue_pellet(width, height)
        elif color == BLUE_FOOD:  # Power pellet 
            self._create_power_pellet(width, height)
        else:  # Special yellow pellet
            self._create_yellow_pellet(width, height)
        
        self.row = row
        self.col = col
        
        # Setup rect position
        self.rect = self.image.get_rect()
        self.rect.top = row * SIZE_WALL + MARGIN["TOP"]
        self.rect.left = col * SIZE_WALL + MARGIN["LEFT"]
        
        # Center the food in the cell
        self.rect.top += SIZE_WALL // 2 - height // 2 - 4
        self.rect.left += SIZE_WALL // 2 - width // 2 - 4
        
        # Animation properties
        self.animation_timer = 0
        self.pulse_size = 0
        self.glow_animation_timer = 0
        self.sparkle_particles = []
        
    def _create_blue_pellet(self, width, height):
        """Tạo viên thức ăn xanh thông thường với hiệu ứng nhẹ nhàng"""
        # Bóng đổ nhỏ hơn
        shadow_surface = pygame.Surface([width + 8, height + 8], pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 50), 
                          [5, 6, width, height])
        self.image.blit(shadow_surface, (0, 0))
        
        # Giảm số lớp glow và phạm vi
        for radius in range(width + 2, width, -1):
            alpha = int(50 * (1 - radius / (width + 2)))
            glow_surface = pygame.Surface([width + 8, height + 8], pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*self.colors['blue_bright'], alpha), 
                             (self.center_x, self.center_y), radius)
            self.image.blit(glow_surface, (0, 0))
        
        # Main pellet with simple gradient
        for y in range(height):
            for x in range(width):
                distance = math.sqrt((x - width/2)**2 + (y - height/2)**2)
                if distance <= width/2:
                    gradient_factor = 1 - (distance / (width/2))
                    
                    if y < height/2:
                        color = self.colors['blue_bright']
                    else:
                        color = self.colors['blue_main']
                    
                    r = int(color[0] * gradient_factor + self.colors['blue_shadow'][0] * (1 - gradient_factor))
                    g = int(color[1] * gradient_factor + self.colors['blue_shadow'][1] * (1 - gradient_factor))
                    b = int(color[2] * gradient_factor + self.colors['blue_shadow'][2] * (1 - gradient_factor))
                    
                    # Hiệu ứng ánh sáng nhẹ nhàng hơn
                    if y < height/3 and x < width*2/3:
                        r = min(255, r + 30)
                        g = min(255, g + 30)
                        b = min(255, b + 30)
                    
                    pixel_surface = pygame.Surface((1, 1), pygame.SRCALPHA)
                    pixel_surface.fill((r, g, b, 255))
                    self.image.blit(pixel_surface, (x + 4, y + 4))
        
        # Highlight nhẹ
        highlight_surface = pygame.Surface([width, height], pygame.SRCALPHA)
        pygame.draw.ellipse(highlight_surface, (255, 255, 255, 100), 
                          [width//3, height//4, width//3, height//3])
        self.image.blit(highlight_surface, (4, 4))
        
        self.sparkle_color = self.colors['blue_bright']
    
    def _create_power_pellet(self, width, height):
        """Tạo power pellet với hiệu ứng xanh sáng hơn"""
        # Bóng đổ nhỏ hơn
        shadow_surface = pygame.Surface([width + 8, height + 8], pygame.SRCALPHA)
        pygame.draw.ellipse(shadow_surface, (0, 0, 0, 70), 
                          [6, 7, width, height])
        self.image.blit(shadow_surface, (0, 0))
        
        # Glow đơn giản hơn
        for radius in range(width + 3, width, -1):
            alpha = int(70 * (1 - radius / (width + 3)))
            glow_surface = pygame.Surface([width + 8, height + 8], pygame.SRCALPHA)
            pygame.draw.circle(glow_surface, (*self.colors['power_blue'], alpha), 
                             (self.center_x, self.center_y), radius)
            self.image.blit(glow_surface, (0, 0))
        
        # Main power pellet với màu xanh sáng
        for y in range(height):
            for x in range(width):
                distance = math.sqrt((x - width/2)**2 + (y - height/2)**2)
                if distance <= width/2:
                    gradient_factor = 1 - (distance / (width/2))
                    
                    if y < height/2:
                        color = self.colors['power_blue']
                    else:
                        color = self.colors['blue_bright']
                    
                    r = int(color[0] * gradient_factor + self.colors['blue_main'][0] * (1 - gradient_factor))
                    g = int(color[1] * gradient_factor + self.colors['blue_main'][1] * (1 - gradient_factor))
                    b = int(color[2] * gradient_factor + self.colors['blue_main'][2] * (1 - gradient_factor))
                    
                    # Hiệu ứng sáng nhẹ
                    if (x - width/2)**2 + (y - height/3)**2 < (width/3)**2:
                        r = min(255, r + 40)
                        g = min(255, g + 40)
                        b = min(255, b + 40)
                    
                    pixel_surface = pygame.Surface((1, 1), pygame.SRCALPHA)
                    pixel_surface.fill((r, g, b, 255))
                    self.image.blit(pixel_surface, (x + 4, y + 4))
        
        highlight_surface = pygame.Surface([width, height], pygame.SRCALPHA)
        pygame.draw.ellipse(highlight_surface, (255, 255, 255, 130), 
                          [width//3, height//4, width//3, height//3])
        self.image.blit(highlight_surface, (4, 4))
        
        self.sparkle_color = self.colors['power_blue']
    
    def _create_yellow_pellet(self, width, height):
        """Tạo viên thức ăn đặc biệt với màu xanh"""
        self._create_power_pellet(width, height)
    
    def _create_sparkle_particles(self, width, height, color):
        """Tạo các hạt lấp lánh nhỏ xung quanh food"""
        for _ in range(3):  # Giảm số lượng hạt
            angle = random.random() * math.pi * 2
            distance = random.random() * (width / 4)  # Giảm phạm vi
            x = self.center_x + math.cos(angle) * distance
            y = self.center_y + math.sin(angle) * distance
            size = random.random() * 2 + 1  # Giảm kích thước
            self.sparkle_particles.append({
                'x': x,
                'y': y,
                'size': size,
                'alpha': 200,  # Giảm độ sáng
                'color': color,
                'lifetime': random.random() * 20 + 20  # Giảm thời gian sống
            })
    
    def draw(self, screen):
        self.animation_timer += 1
        
        # Animation nhẹ nhàng hơn
        if self.base_color == YELLOW:  # Power pellet
            self.pulse_size = math.sin(self.animation_timer * 0.1) * 1 + 1  # Giảm biên độ
            
            pulse_surface = pygame.Surface([self.image.get_width() + 4, self.image.get_height() + 4], pygame.SRCALPHA)
            pulse_radius = self.image.get_width() // 2 + self.pulse_size + 2
            pygame.draw.circle(pulse_surface, (*self.colors['power_glow'][:3], 30),
                             (self.image.get_width() // 2 + 2, self.image.get_height() // 2 + 2), 
                             pulse_radius)
            
            screen.blit(pulse_surface, (self.rect.left - self.pulse_size - 2, 
                                      self.rect.top - self.pulse_size - 2))
        
        elif self.base_color == WHITE:  # Blue pellet
            self.glow_animation_timer += 1
            glow_intensity = math.sin(self.glow_animation_timer * 0.06) * 20 + 60  # Giảm biên độ và intensity
            
            glow_surface = pygame.Surface([self.image.get_width() + 4, self.image.get_height() + 4], pygame.SRCALPHA)
            center_x = self.image.get_width() // 2 + 2
            center_y = self.image.get_height() // 2 + 2
            
            # Chỉ một lớp glow mỏng
            radius = self.image.get_width() // 2 + 2
            alpha = int(glow_intensity)
            pygame.draw.circle(glow_surface, (*self.colors['glow_blue'][:3], alpha),
                             (center_x, center_y), radius)
            
            screen.blit(glow_surface, (self.rect.left - 2, self.rect.top - 2))
        
        # Draw sparkle particles nhẹ nhàng hơn
        for particle in self.sparkle_particles:
            particle['lifetime'] -= 1
            particle['alpha'] = int(200 * (particle['lifetime'] / 40))  # Fade mềm mại hơn
            
            if particle['lifetime'] > 0:
                sparkle_surface = pygame.Surface([3, 3], pygame.SRCALPHA)
                color_with_alpha = particle['color'] + (particle['alpha'],)
                pygame.draw.circle(sparkle_surface, color_with_alpha, 
                                 (1, 1), particle['size'])
                screen.blit(sparkle_surface, 
                          (particle['x'] + self.rect.left - 1 - self.center_x + 4, 
                           particle['y'] + self.rect.top - 1 - self.center_y + 4))
        
        self.sparkle_particles = [p for p in self.sparkle_particles if p['lifetime'] > 0]
        
        # Tạo particles mới ít thường xuyên hơn
        if self.animation_timer % 45 == 0 and hasattr(self, 'sparkle_color'):
            self._create_sparkle_particles(8, 8, self.sparkle_color)
        
        # Draw main food
        screen.blit(self.image, (self.rect.left, self.rect.top))
    
    def getRC(self):
        return [self.row, self.col]