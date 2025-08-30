import pygame
from UI_helpers.ui_theme import CARD_BG, CARD_STROKE, COLOR_TEXT, ACCENT_2, draw_rounded_rect, render_with_shadow

def draw_company_card(screen, rect, empresa, font_title, font_meta, highlight=False):
    r = pygame.Rect(rect)
    draw_rounded_rect(screen, r, CARD_BG, radius=16, border=2, border_color=CARD_STROKE)
    if highlight:
        pygame.draw.rect(screen, ACCENT_2, r, width=3, border_radius=16)

    title = render_with_shadow(font_title, empresa.nombre, COLOR_TEXT, (0,0,0))
    meta1  = font_meta.render(f"${empresa.valor_base}", True, COLOR_TEXT)
    meta2  = font_meta.render(empresa.industria, True, COLOR_TEXT)

    screen.blit(title, (r.x+14, r.y+10))
    screen.blit(meta1,  (r.x+14, r.y+12 + title.get_height()))
    screen.blit(meta2,  (r.x+14, r.y+18 + title.get_height()+meta1.get_height()))
