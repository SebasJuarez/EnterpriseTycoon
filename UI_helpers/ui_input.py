import pygame
from UI_helpers.ui_theme import CARD_BG, CARD_STROKE, COLOR_TEXT, draw_rounded_rect

class UIInput:
    def __init__(self, rect, font, text=""):
        self.rect = pygame.Rect(rect)
        self.font = font
        self.text = text
        self.active = False

    def handle(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        if self.active and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.key == pygame.K_RETURN:
                self.active = False
            else:
                self.text += event.unicode

    def draw(self, screen):
        draw_rounded_rect(screen, self.rect, CARD_BG, radius=10, border=2, border_color=CARD_STROKE)
        label = self.font.render(self.text or "", True, COLOR_TEXT)
        screen.blit(label, (self.rect.x+12, self.rect.y+(self.rect.h-label.get_height())//2))
