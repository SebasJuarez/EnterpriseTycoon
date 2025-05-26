import pygame
import sys
import random
from jugador import Jugador, IAJugador
from mundo import MundoEmpresarial

pygame.init()

# --- Configuraciones ---
ANCHO, ALTO = 800, 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Simulador Empresarial")

FUENTE = pygame.font.SysFont("arial", 32)
FUENTE_INPUT = pygame.font.SysFont("arial", 28)
FUENTE_SMALL = pygame.font.SysFont("arial", 24)
COLOR_FONDO = (30, 30, 30)
COLOR_TEXTO = (255, 255, 255)
COLOR_BOTON = (50, 50, 150)
COLOR_HOVER = (70, 70, 200)
COLOR_INPUT = (255, 255, 255)
COLOR_INPUT_BG = (50, 50, 50)

clock = pygame.time.Clock()

OBJETIVOS_SECRETOS = [
    {
        "descripcion": "Controlar al menos 2 empresas del mismo tipo",
        "pista": "Hay un final secreto para quien logre un monopolio de algún tipo...",
        "condicion": lambda j: any(c >= 2 for c in j.contar_por_tipo().values())
    },
    {
        "descripcion": "Tener al menos $6000 de dinero en efectivo",
        "pista": "Se rumorea que la liquidez trae la victoria...",
        "condicion": lambda j: j.dinero >= 6000
    },
    {
        "descripcion": "Poseer una empresa con una ventaja especial que incluya la palabra 'Dominio'",
        "pista": "Algunos dicen que dominar un sector es clave para la victoria...",
        "condicion": lambda j: any(e.ventaja and "Dominio" in e.ventaja for e in j.empresas)
    },
    {
        "descripcion": "Tener exactamente 3 empresas",
        "pista": "¿Y si el número perfecto fuera 3?",
        "condicion": lambda j: len(j.empresas) == 3
    },
    {
        "descripcion": "Tener al menos una empresa de cada tipo disponible en la partida",
        "pista": "Diversificar podría tener sus recompensas ocultas...",
        "condicion": lambda j: len(j.contar_por_tipo()) >= 4
    },
]

# --- Botones ---
class Boton:
    def __init__(self, texto, x, y, w, h, accion):
        self.texto = texto
        self.rect = pygame.Rect(x, y, w, h)
        self.accion = accion

    def dibujar(self, superficie):
        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()
        color = COLOR_HOVER if self.rect.collidepoint(mouse) else COLOR_BOTON
        pygame.draw.rect(superficie, color, self.rect)
        texto_render = FUENTE.render(self.texto, True, COLOR_TEXTO)
        superficie.blit(texto_render, (self.rect.x + 20, self.rect.y + 10))

        if self.rect.collidepoint(mouse) and click[0] == 1:
            pygame.time.delay(200)
            self.accion()

# --- Funciones de menú ---
def jugar():
    ingresar_nombre()

def partida_ia():
    ia_0 = IAJugador("NeuroCorp", 5000, "pasiva")
    ia_1 = IAJugador("CorpX", 5000, "acaparadora")
    ia_2 = IAJugador("MegaTech", 5000, "agresiva")
    jugadores = [ia_0, ia_1, ia_2]
    ejecutar_juego(jugadores)

def ver_reporte():
    print("Mostrar reporte de aprendizaje IA...")

def ingresar_nombre():
    nombre = ""
    activo = True
    input_box = pygame.Rect(250, 280, 300, 50)

    while activo:
        VENTANA.fill(COLOR_FONDO)
        titulo = FUENTE.render("Ingresa tu nombre:", True, COLOR_TEXTO)
        VENTANA.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 200))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_RETURN:
                    jugador_humano = Jugador(nombre, 5000)
                    ia_1 = IAJugador("CorpX", 5000, "acaparadora")
                    ia_2 = IAJugador("MegaTech", 5000, "agresiva")
                    jugadores = [jugador_humano, ia_1, ia_2]
                    activo = False
                    ejecutar_juego(jugadores)
                elif evento.key == pygame.K_BACKSPACE:
                    nombre = nombre[:-1]
                else:
                    if len(nombre) < 20:
                        nombre += evento.unicode

        pygame.draw.rect(VENTANA, COLOR_INPUT_BG, input_box)
        texto_nombre = FUENTE_INPUT.render(nombre, True, COLOR_INPUT)
        VENTANA.blit(texto_nombre, (input_box.x + 10, input_box.y + 10))
        pygame.draw.rect(VENTANA, COLOR_TEXTO, input_box, 2)

        pygame.display.flip()
        clock.tick(60)

COLORES_TIPO = {
    "tecnologia": (0, 150, 255),
    "salud": (255, 100, 100),
    "medios": (255, 255, 0),
    "finanzas": (100, 255, 100),
    "entretenimiento": (255, 100, 255),
    "energia": (255, 150, 50),
    "inmobiliario": (200, 200, 200)
}

COLORES_JUGADORES = [(255, 100, 100), (100, 255, 100), (100, 100, 255)]

def ejecutar_juego(jugadores):
    juego = MundoEmpresarial(jugadores)
    objetivo_secreto = random.choice(OBJETIVOS_SECRETOS)

    for ronda in range(1, 6):
        juego.ejecutar_ronda()

        VENTANA.fill(COLOR_FONDO)

        titulo = FUENTE.render(f"Ronda {ronda}", True, COLOR_TEXTO)
        pista = FUENTE_SMALL.render(f"🔍 Pista: {objetivo_secreto['pista']}", True, COLOR_TEXTO)
        VENTANA.blit(titulo, (50, 30))
        VENTANA.blit(pista, (50, 80))

        for idx, jugador in enumerate(juego.jugadores):
            color = COLORES_JUGADORES[idx % len(COLORES_JUGADORES)]
            info = f"{jugador.nombre} | Dinero: ${jugador.dinero} | Empresas: {', '.join([e.nombre for e in jugador.empresas])}"
            render = FUENTE_SMALL.render(info, True, color)
            VENTANA.blit(render, (50, 140 + idx * 40))

        # Mostrar empresas como tarjetas
        empresas_texto = FUENTE_SMALL.render("🛒 Empresas disponibles:", True, COLOR_TEXTO)
        VENTANA.blit(empresas_texto, (50, 300))

        for i, emp in enumerate(juego.empresas_disponibles):
            x, y = 50 + (i % 3) * 250, 340 + (i // 3) * 100
            ancho, alto = 200, 80
            color_fondo = COLORES_TIPO.get(emp.tipo, (150, 150, 150))

            # Fondo de tarjeta
            pygame.draw.rect(VENTANA, color_fondo, (x, y, ancho, alto), border_radius=8)
            pygame.draw.rect(VENTANA, (255, 255, 255), (x, y, ancho, alto), 2, border_radius=8)

            nombre = FUENTE_SMALL.render(emp.nombre, True, (0, 0, 0))
            valor = FUENTE_SMALL.render(f"${emp.valor}", True, (0, 0, 0))
            tipo = FUENTE_SMALL.render(f"{emp.tipo}", True, (0, 0, 0))

            VENTANA.blit(nombre, (x + 10, y + 5))
            VENTANA.blit(valor, (x + 10, y + 30))
            VENTANA.blit(tipo, (x + 10, y + 55))

            if emp.ventaja:
                ventaja = FUENTE_SMALL.render("★", True, (0, 0, 0))
                VENTANA.blit(ventaja, (x + ancho - 25, y + 5))

        pygame.display.flip()
        pygame.time.delay(2500)

    # Mostrar resultado final
    VENTANA.fill(COLOR_FONDO)
    titulo = FUENTE.render("🏆 RESULTADOS FINALES:", True, COLOR_TEXTO)
    VENTANA.blit(titulo, (50, 30))

    ganador_secreto = None
    for j in juego.jugadores:
        if objetivo_secreto["condicion"](j):
            ganador_secreto = j
            break

    if ganador_secreto:
        texto = FUENTE_SMALL.render(f"🎉 ¡{ganador_secreto.nombre} cumplió el objetivo secreto!", True, COLOR_TEXTO)
        VENTANA.blit(texto, (50, 100))
        texto2 = FUENTE_SMALL.render(f"🔐 Objetivo: {objetivo_secreto['descripcion']}", True, COLOR_TEXTO)
        VENTANA.blit(texto2, (50, 140))
    else:
        jugadores_ordenados = sorted(juego.jugadores, key=lambda j: j.valor_total(), reverse=True)
        for i, j in enumerate(jugadores_ordenados):
            texto = FUENTE_SMALL.render(f"{i+1}. {j.nombre} - Valor total: ${j.valor_total()}", True, COLOR_TEXTO)
            VENTANA.blit(texto, (50, 100 + i * 40))

    pygame.display.flip()
    pygame.time.delay(5000)


def menu():
    botones = [
        Boton("Jugar", 300, 200, 200, 50, jugar),
        Boton("Ver partida de IAs", 300, 280, 200, 50, partida_ia),
        Boton("Ver reporte de aprendizaje", 300, 360, 200, 50, ver_reporte)
    ]

    corriendo = True
    while corriendo:
        VENTANA.fill(COLOR_FONDO)

        titulo = FUENTE.render("Simulador Empresarial", True, COLOR_TEXTO)
        VENTANA.blit(titulo, (ANCHO // 2 - titulo.get_width() // 2, 100))

        for boton in botones:
            boton.dibujar(VENTANA)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                corriendo = False

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()

# --- Iniciar el menú ---
if __name__ == "__main__":
    menu()
