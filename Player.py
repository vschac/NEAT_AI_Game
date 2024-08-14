import Components
import math
import pygame
from Enemy import Enemy
from Projectile import Projectile

class Player:
    SPEED = 10
    FIRE_COOLDOWN = Components.FPS * 4

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rot = 90
        self.projectiles = []
        self.last_fired = 0
        self.health = 5
        self.lowestEnemy = Enemy(Components.WIN_WIDTH/2, Components.WIN_HEIGHT/2)
    
    def draw(self, win):
        point1 = (self.x + 20 * math.cos(math.radians(self.rot)), self.y - 20 * math.sin(math.radians(self.rot)))
        point2 = (self.x + 20 * math.cos(math.radians(self.rot + 120)), self.y - 20 * math.sin(math.radians(self.rot + 120)))
        point3 = (self.x + 20 * math.cos(math.radians(self.rot + 240)), self.y - 20 * math.sin(math.radians(self.rot + 240)))
        pygame.draw.polygon(win, (255, 0, 0), [point1, point2, point3])

    def move(self, dir):
        if dir == 1:
            self.x -= self.SPEED
        if dir == 2:
            self.x += self.SPEED
        if self.x <= 0:
            self.x = 1
        if self.x >= Components.WIN_WIDTH:
            self.x = Components.WIN_WIDTH - 1

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_fired >= self.FIRE_COOLDOWN:
            direction = math.radians(self.rot)
            self.projectiles.append(Projectile(self.x, self.y, direction, 10))
            self.last_fired = current_time

    def get_bounding_box(self):
        return pygame.Rect(self.x - 20, self.y - 20, 40, 40)