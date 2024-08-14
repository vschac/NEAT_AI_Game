import pygame

pygame.font.init()
BUTTON_FONT = pygame.font.SysFont("comicsans", 15)

FPS = 60
WIN_WIDTH = 600
WIN_HEIGHT = 600

class Button:
    def __init__(self, x, y, width, height, text, font, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.font = font
        self.color = color
        self.hover_color = hover_color
        self.current_color = color

    def draw(self, win):
        pygame.draw.rect(win, self.current_color, self.rect)
        text_surface = self.font.render(self.text, True, (255, 255, 255))
        win.blit(text_surface, (self.rect.x + (self.rect.width - text_surface.get_width()) // 2,
                                self.rect.y + (self.rect.height - text_surface.get_height()) // 2))

    def is_hovered(self, mouse_pos):
        return self.rect.collidepoint(mouse_pos)

    def is_clicked(self, mouse_pos):
        return self.is_hovered(mouse_pos)
