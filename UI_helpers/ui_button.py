import pygame
from UI_helpers.ui_theme import BTN_BG, BTN_BG_HOVER, COLOR_TEXT, draw_rounded_rect, render_with_shadow

class UIButton:
    def __init__(self, rect, text, font, on_click, radius=14):
        self.rect = pygame.Rect(rect)
        self.text = text
        self.font = font
        self.on_click = on_click
        self.radius = radius
        self.hover = False

    def handle(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()

    def draw(self, screen):
        bg = BTN_BG_HOVER if self.hover else BTN_BG
        draw_rounded_rect(screen, self.rect, bg, radius=self.radius, border=2)
        label = render_with_shadow(self.font, self.text, COLOR_TEXT, (0,0,0))
        screen.blit(label, (self.rect.centerx - label.get_width()//2,
                            self.rect.centery - label.get_height()//2))
