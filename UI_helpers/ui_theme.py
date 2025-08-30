import pygame
from pygame import Surface

# ====== Colores del tema (oscuro + acentos neón) ======
COLOR_BG        = (16, 16, 18)
COLOR_TEXT      = (235, 235, 235)
ACCENT_1        = (255, 102, 255)   # rosa neón
ACCENT_2        = (0, 255, 170)     # verde menta
CARD_BG         = (27, 27, 31)
CARD_STROKE     = (210, 210, 210)
BTN_BG          = (51, 51, 120)
BTN_BG_HOVER    = (70, 70, 160)

# ====== Fuentes ======
def load_font(path, size):
    try:
        return pygame.font.Font(path, size)
    except:
        return pygame.font.SysFont("arial", size, bold=True)

# ====== Helpers de dibujo ======
def draw_rounded_rect(surf, rect, color, radius=12, border=0, border_color=(0,0,0)):
    pygame.draw.rect(surf, color, rect, border_radius=radius)
    if border > 0:
        pygame.draw.rect(surf, border_color, rect, width=border, border_radius=radius)

def blit_shadow(surf, child, pos, spread=6, alpha=80):
    """Sombra soft: duplica la superficie y la difumina via escalado."""
    x, y = pos
    w, h = child.get_size()
    shadow = pygame.transform.smoothscale(child, (w+spread, h+spread))
    shadow.fill((0,0,0,alpha), special_flags=pygame.BLEND_RGBA_MULT)
    surf.blit(shadow, (x- spread//4, y- spread//4))

def render_with_shadow(font, text, color, shadow_color=(0,0,0), off=(3,3)):
    base = font.render(text, True, color)
    shadow = font.render(text, True, shadow_color)
    w, h = base.get_size()
    s = Surface((w+abs(off[0]), h+abs(off[1])), pygame.SRCALPHA)
    s.blit(shadow, (max(off[0],0), max(off[1],0)))
    s.blit(base, (0,0))
    return s

def render_neon(font, text, main=ACCENT_1, glow=ACCENT_2, glow_layers=3):
    """Efecto neón sencillo: capas crecientes con alpha."""
    base = font.render(text, True, main)
    w, h = base.get_size()
    s = Surface((w+20, h+20), pygame.SRCALPHA)
    cx, cy = 10, 10
    for i in range(glow_layers, 0, -1):
        g = font.render(text, True, glow)
        g = pygame.transform.smoothscale(g, (int(g.get_width()*1.02*i/glow_layers),
                                             int(g.get_height()*1.02*i/glow_layers)))
        g.set_alpha(50 // i + 20)
        s.blit(g, (cx - (g.get_width()-base.get_width())//2,
                   cy - (g.get_height()-base.get_height())//2))
    s.blit(base, (cx, cy))
    return s

def lerp(a, b, t): return a + (b-a)*t
