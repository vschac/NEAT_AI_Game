import math
import pygame

class Projectile:
    def __init__(self, x, y, direction, speed):
        self.x = x
        self.y = y
        self.direction = direction
        self.SPEED = speed
    
    def move(self):
        self.y -= self.SPEED * math.sin(self.direction)

    def draw(self, win):
        pygame.draw.circle(win, (255, 255, 0), (int(self.x), int(self.y)), 5)

    def get_bounding_box(self):
        return pygame.Rect(self.x - 2.5, self.y - 2.5, 5, 5)