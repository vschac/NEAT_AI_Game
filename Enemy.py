import Components
import pygame

class Enemy(object):
    FIRE_COOLDOWN = Components.FPS * 15
    SPEED = 0.1

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.last_fired = 0

    def draw(self, win):
        pygame.draw.rect(win, (0, 0, 255), (self.x - 20, self.y - 20, 40, 40))

    def move(self):
        self.y += self.SPEED

    def get_bounding_box(self):
        return pygame.Rect(self.x - 20, self.y - 20, 40, 40)