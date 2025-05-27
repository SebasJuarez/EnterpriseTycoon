import pygame
import sys
import random
import csv
from collections import defaultdict
import statistics
from jugador import Jugador, IAJugador
from mundo import MundoEmpresarial

pygame.init()
registro_ia = []  # Guardará los datos por ronda
# --- Configuraciones ---
ANCHO, ALTO = 1000, 800
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

def jugar():
    ingresar_nombre()

def partida_ia():
    ia_0 = IAJugador("NeuroCorp", 5000, "pasiva")
    ia_1 = IAJugador("CorpX", 5000, "acaparadora")
    ia_2 = IAJugador("MegaTech", 5000, "agresiva")
    jugadores = [ia_0, ia_1, ia_2]
    ejecutar_juego_ia(jugadores)

def ver_reporte():
    if not registro_ia:
        print("No hay datos registrados.")
        return

    with open("reporte_ia.csv", "w", newline="", encoding="utf-8") as f:
        campos = registro_ia[0].keys()
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        for fila in registro_ia:
            writer.writerow(fila)

    print("Reporte generado como 'reporte_ia.csv'")

    # --- Análisis de IA ---
    resumen = defaultdict(lambda: {
        "rondas": 0,
        "dinero_final": 0,
        "valor_total": [],
        "empresas": [],
        "tipos": set(),
        "objetivos_cumplidos": 0
    })

    for fila in registro_ia:
        nombre = fila["nombre"]
        resumen[nombre]["rondas"] += 1
        resumen[nombre]["dinero_final"] = fila["dinero"]
        resumen[nombre]["valor_total"].append(fila["valor_total"])
        resumen[nombre]["empresas"].append(fila["empresas"])
        resumen[nombre]["tipos"].update(fila["tipos"])
        if fila.get("objetivo_secreto_cumplido"):
            resumen[nombre]["objetivos_cumplidos"] += 1

    print("\n📊 INSIGHTS DEL COMPORTAMIENTO DE LAS IAs:\n")
    for nombre, datos in resumen.items():
        promedio_valor = statistics.mean(datos["valor_total"])
        promedio_empresas = statistics.mean(datos["empresas"])
        tipos = len(datos["tipos"])
        print(f"🔹 {nombre}")
        print(f"   • Promedio de valor total: ${promedio_valor:.2f}")
        print(f"   • Promedio de empresas por ronda: {promedio_empresas:.2f}")
        print(f"   • Tipos distintos de empresas que tuvo: {tipos}")
        print(f"   • Dinero al final: ${datos['dinero_final']}")
        print(f"   • Veces que cumplió el objetivo secreto: {datos['objetivos_cumplidos']}/{datos['rondas']}")
        print("")

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
        VENTANA.fill(COLOR_FONDO)

        titulo = FUENTE.render(f"Ronda {ronda}", True, COLOR_TEXTO)
        pista = FUENTE_SMALL.render(f"🔍 Pista: {objetivo_secreto['pista']}", True, COLOR_TEXTO)
        VENTANA.blit(titulo, (50, 30))
        VENTANA.blit(pista, (50, 80))

        # Generar nuevas empresas esta ronda
        juego.generar_empresas()

        # Mostrar jugadores antes de tomar turnos
        for idx, jugador in enumerate(juego.jugadores):
            color = COLORES_JUGADORES[idx % len(COLORES_JUGADORES)]
            info = f"{jugador.nombre} | Dinero: ${jugador.dinero} | Empresas: {', '.join([e.nombre for e in jugador.empresas])}"
            render = FUENTE_SMALL.render(info, True, color)
            VENTANA.blit(render, (50, 140 + idx * 40))
        
        # Botón de vender empresa/saltar turno
        boton_vender = pygame.Rect(600, 30, 160, 40)
        boton_saltar = pygame.Rect(780, 30, 160, 40)

        pygame.draw.rect(VENTANA, COLOR_BOTON, boton_vender, border_radius=5)
        pygame.draw.rect(VENTANA, COLOR_BOTON, boton_saltar, border_radius=5)

        texto_vender = FUENTE_SMALL.render("Vender Empresa", True, COLOR_TEXTO)
        texto_saltar = FUENTE_SMALL.render("Saltar Turno", True, COLOR_TEXTO)

        VENTANA.blit(texto_vender, (boton_vender.x + 10, boton_vender.y + 10))
        VENTANA.blit(texto_saltar, (boton_saltar.x + 20, boton_saltar.y + 10))


        # Mostrar empresas como tarjetas
        empresas_texto = FUENTE_SMALL.render("🛒 Empresas disponibles:", True, COLOR_TEXTO)
        VENTANA.blit(empresas_texto, (50, 300))

        empresa_rects = []  # Guardar cada rect con su empresa

        for i, emp in enumerate(juego.empresas_disponibles):
            x, y = 50 + (i % 3) * 250, 340 + (i // 3) * 100
            ancho, alto = 200, 80
            color_fondo = COLORES_TIPO.get(emp.tipo, (150, 150, 150))

            rect = pygame.Rect(x, y, ancho, alto)
            empresa_rects.append((rect, emp))

            pygame.draw.rect(VENTANA, color_fondo, rect, border_radius=8)
            pygame.draw.rect(VENTANA, (255, 255, 255), rect, 2, border_radius=8)

            nombre = FUENTE_SMALL.render(emp.nombre, True, (0, 0, 0))
            valor = FUENTE_SMALL.render(f"${emp.valor}", True, (0, 0, 0))
            tipo = FUENTE_SMALL.render(f"{emp.tipo}", True, (0, 0, 0))

            VENTANA.blit(nombre, (x + 10, y + 5))
            VENTANA.blit(valor, (x + 10, y + 30))
            VENTANA.blit(tipo, (x + 10, y + 55))

            if emp.ventaja:
                estrella = FUENTE_SMALL.render("★", True, (0, 0, 0))
                VENTANA.blit(estrella, (x + ancho - 25, y + 5))

        pygame.display.flip()

        # Turno del jugador humano
        jugador_humano = next((j for j in juego.jugadores if isinstance(j, Jugador)), None)
        if jugador_humano:
            esperando = True
            while esperando:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                        pos = pygame.mouse.get_pos()
                        for rect, emp in empresa_rects:
                            if rect.collidepoint(pos):
                                iniciar_subasta(emp, juego.jugadores, VENTANA, FUENTE, FUENTE_SMALL, COLOR_FONDO, COLOR_TEXTO, COLOR_INPUT_BG, COLOR_INPUT)
                                juego.empresas_disponibles.remove(emp)
                                esperando = False
                                break
                            elif boton_vender.collidepoint(pos):
                                resultado = seleccionar_empresa_para_vender(jugador_humano)
                                if resultado:
                                    empresa, precio_venta = resultado
                                    jugador_humano.vender_empresa(empresa.nombre, precio_venta)

                                    confirmacion = FUENTE_SMALL.render(f"Vendiste {empresa.nombre} por ${precio_venta}", True, COLOR_TEXTO)
                                    VENTANA.blit(confirmacion, (50, 550))
                                    pygame.display.flip()
                                    pygame.time.delay(1500)
                                esperando = False
                            elif boton_saltar.collidepoint(pos):
                                esperando = False
                                break


        # Turnos de las IAs (después del jugador)
        for jugador in juego.jugadores:
            if isinstance(jugador, IAJugador):
                # Decidir si vender antes de tomar turno
                ventas = decidir_ventas_ia(jugador)
                for empresa, precio, razon in ventas:
                    jugador.empresas.remove(empresa)
                    jugador.dinero += precio  # Simulamos venta inmediata
                    # (Opcional) podrías agregar un registro visual o imprimir algo:
                    print(f"{jugador.nombre} vendió {empresa.nombre} por ${precio} ({razon})")
                
                jugador.tomar_turno(juego.empresas_disponibles, juego.jugadores, juego)

        juego.empresas_disponibles = [e for e in juego.empresas_disponibles if e.esta_disponible()]
        for jugador in juego.jugadores:
            aplicar_ventajas(jugador)
        juego.ronda += 1

    # Mostrar resultado final
    VENTANA.fill(COLOR_FONDO)
    titulo = FUENTE.render("RESULTADOS FINALES:", True, COLOR_TEXTO)
    VENTANA.blit(titulo, (50, 30))

    ganador_secreto = None
    for j in juego.jugadores:
        if objetivo_secreto["condicion"](j):
            ganador_secreto = j
            break

    if ganador_secreto:
        texto = FUENTE_SMALL.render(f"¡{ganador_secreto.nombre} cumplió el objetivo secreto!", True, COLOR_TEXTO)
        VENTANA.blit(texto, (50, 100))
        texto2 = FUENTE_SMALL.render(f"Objetivo: {objetivo_secreto['descripcion']}", True, COLOR_TEXTO)
        VENTANA.blit(texto2, (50, 140))
    else:
        jugadores_ordenados = sorted(juego.jugadores, key=lambda j: j.valor_total(), reverse=True)
        for i, j in enumerate(jugadores_ordenados):
            texto = FUENTE_SMALL.render(f"{i+1}. {j.nombre} - Valor total: ${j.valor_total()}", True, COLOR_TEXTO)
            VENTANA.blit(texto, (50, 100 + i * 40))

    pygame.display.flip()
    pygame.time.delay(5000)

def seleccionar_empresa_para_vender(jugador):
    if not jugador.empresas:
        return None

    seleccionando = True
    empresa_rects = []
    empresa_seleccionada = None
    precio_input = ""
    input_box = pygame.Rect(50, 600, 200, 40)
    boton_confirmar = pygame.Rect(270, 600, 120, 40)
    boton_cancelar = pygame.Rect(800, 700, 150, 40)

    while seleccionando:
        VENTANA.fill(COLOR_FONDO)
        titulo = FUENTE.render("Selecciona empresa a vender", True, COLOR_TEXTO)
        VENTANA.blit(titulo, (50, 30))

        empresa_rects.clear()
        for i, emp in enumerate(jugador.empresas):
            x, y = 50, 100 + i * 80
            rect = pygame.Rect(x, y, 700, 60)
            empresa_rects.append((rect, emp))
            pygame.draw.rect(VENTANA, COLORES_TIPO.get(emp.tipo, (100, 100, 100)), rect, border_radius=5)
            pygame.draw.rect(VENTANA, (255, 255, 255), rect, 2, border_radius=5)
            texto = f"{emp.nombre} ({emp.tipo}) - Valor: ${emp.valor}"
            VENTANA.blit(FUENTE_SMALL.render(texto, True, COLOR_TEXTO), (x + 10, y + 15))

        # Si ya seleccionó una empresa, mostrar campo para ingresar precio
        if empresa_seleccionada:
            msg = FUENTE_SMALL.render(f"Ingresa precio para vender {empresa_seleccionada.nombre}:", True, COLOR_TEXTO)
            VENTANA.blit(msg, (50, 560))

            pygame.draw.rect(VENTANA, COLOR_INPUT_BG, input_box)
            texto_input = FUENTE_SMALL.render(precio_input, True, COLOR_INPUT)
            VENTANA.blit(texto_input, (input_box.x + 10, input_box.y + 5))
            pygame.draw.rect(VENTANA, COLOR_TEXTO, input_box, 2)

            # Botón confirmar
            pygame.draw.rect(VENTANA, COLOR_BOTON, boton_confirmar, border_radius=5)
            texto_conf = FUENTE_SMALL.render("Confirmar", True, COLOR_TEXTO)
            VENTANA.blit(texto_conf, (boton_confirmar.x + 10, boton_confirmar.y + 10))

        # Botón cancelar
        pygame.draw.rect(VENTANA, COLOR_BOTON, boton_cancelar, border_radius=5)
        texto_cancelar = FUENTE_SMALL.render("Cancelar", True, COLOR_TEXTO)
        VENTANA.blit(texto_cancelar, (boton_cancelar.x + 30, boton_cancelar.y + 10))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                pos = pygame.mouse.get_pos()

                if boton_cancelar.collidepoint(pos):
                    return None

                if empresa_seleccionada and boton_confirmar.collidepoint(pos):
                    try:
                        precio = int(precio_input)
                        return (empresa_seleccionada, precio)
                    except:
                        precio_input = ""
                        continue

                for rect, emp in empresa_rects:
                    if rect.collidepoint(pos):
                        empresa_seleccionada = emp
                        precio_input = ""

            elif evento.type == pygame.KEYDOWN and empresa_seleccionada:
                if evento.key == pygame.K_BACKSPACE:
                    precio_input = precio_input[:-1]
                elif evento.key == pygame.K_RETURN:
                    try:
                        precio = int(precio_input)
                        return (empresa_seleccionada, precio)
                    except:
                        precio_input = ""
                elif evento.unicode.isdigit():
                    if len(precio_input) < 7:
                        precio_input += evento.unicode

def aplicar_ventajas(jugador):
    for empresa in jugador.empresas:
        if empresa.ventaja:
            texto = f"{jugador.nombre} recibe beneficio por '{empresa.ventaja}'"
            beneficio = ""

            if "Dominio" in empresa.ventaja:
                jugador.dinero += 300
                beneficio = "+$300 por dominio de sector"
            elif "Innovadora" in empresa.ventaja:
                empresa.valor = int(empresa.valor * 1.10)
                beneficio = "+10% al valor de la empresa"
            elif "Alta Demanda" in empresa.ventaja:
                jugador.dinero += 150
                beneficio = "+$150 por ingresos extras"
            elif "Estable" in empresa.ventaja:
                jugador.dinero += 100
                beneficio = "+$100 por estabilidad"
            elif "Reputación" in empresa.ventaja:
                jugador.dinero += 200
                beneficio = "+$200 por buena imagen"

            if beneficio:
                # Mostrar en pantalla
                VENTANA.fill(COLOR_FONDO)
                msg1 = FUENTE_SMALL.render(texto, True, COLOR_TEXTO)
                msg2 = FUENTE_SMALL.render(beneficio, True, COLOR_TEXTO)
                VENTANA.blit(msg1, (50, 300))
                VENTANA.blit(msg2, (50, 340))
                pygame.display.flip()
                pygame.time.delay(2000)


def iniciar_subasta(empresa, jugadores, ventana, fuente, fuente_small, color_fondo, color_texto, color_input_bg, color_input):
    oferta_actual = empresa.valor // 2
    mejor_postor = None
    input_box = pygame.Rect(50, 600, 200, 40)
    oferta_input = ""
    turno_humano = True
    subasta_en_curso = True
    retirado = False
    reloj = pygame.time.Clock()

    jugador_humano = next(j for j in jugadores if isinstance(j, Jugador))

    mensaje_ia = ""
    mensaje_cancelado = False

    while subasta_en_curso:
        ventana.fill(color_fondo)
        titulo = fuente.render(f"Subasta: {empresa.nombre}", True, color_texto)
        valor_base = fuente_small.render(f"Valor base: ${empresa.valor}", True, color_texto)
        oferta = fuente_small.render(f"Oferta actual: ${oferta_actual}", True, color_texto)

        ventana.blit(titulo, (50, 30))
        ventana.blit(valor_base, (50, 80))
        ventana.blit(oferta, (50, 120))

        y_base = 180
        for j in jugadores:
            info = f"{j.nombre} - Dinero: ${j.dinero}"
            ventana.blit(fuente_small.render(info, True, color_texto), (50, y_base))
            y_base += 30

        if turno_humano and not retirado:
            msg = fuente_small.render("Tu oferta (0 para salir):", True, color_texto)
            ventana.blit(msg, (50, 560))

            pygame.draw.rect(ventana, color_input_bg, input_box)
            texto_input = fuente_small.render(oferta_input, True, color_input)
            ventana.blit(texto_input, (input_box.x + 10, input_box.y + 5))
            pygame.draw.rect(ventana, color_texto, input_box, 2)

        if mensaje_ia:
            ventana.blit(fuente_small.render(mensaje_ia, True, color_texto), (50, 500))

        if mensaje_cancelado:
            ventana.blit(fuente_small.render("Nadie ofertó. Subasta cancelada.", True, color_texto), (50, 500))

        pygame.display.flip()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if turno_humano and not retirado:
                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        try:
                            nueva_oferta = int(oferta_input)
                            if nueva_oferta == 0:
                                retirado = True
                                turno_humano = False
                                oferta_input = ""
                                break
                            elif nueva_oferta > oferta_actual and nueva_oferta <= jugador_humano.dinero:
                                oferta_actual = nueva_oferta
                                mejor_postor = jugador_humano
                                turno_humano = False
                                oferta_input = ""
                                mensaje_ia = ""
                        except:
                            oferta_input = ""
                    elif evento.key == pygame.K_BACKSPACE:
                        oferta_input = oferta_input[:-1]
                    elif evento.unicode.isdigit():
                        if len(oferta_input) < 7:
                            oferta_input += evento.unicode

        if not turno_humano:
            pygame.time.delay(700)
            pujado = False
            mensaje_ia = ""
            for ia in [j for j in jugadores if isinstance(j, IAJugador)]:
                if ia.dinero > oferta_actual + 100:
                    if random.random() < 0.6:
                        nueva_oferta = oferta_actual + 100
                        oferta_actual = nueva_oferta
                        mejor_postor = ia
                        pujado = True
                        mensaje_ia = f"{ia.nombre} ofrece ${oferta_actual}"
                        break
            if not pujado:
                if mejor_postor is None:
                    mensaje_cancelado = True
                    pygame.display.flip()
                    pygame.time.delay(2000)
                subasta_en_curso = False
            else:
                if not retirado:
                    turno_humano = True

        reloj.tick(60)

    if mejor_postor:
        mejor_postor.dinero -= oferta_actual
        mejor_postor.empresas.append(empresa)
        empresa.propietario = mejor_postor
        ventana.fill(color_fondo)
        msg = fuente.render(f"{mejor_postor.nombre} ganó la subasta por ${oferta_actual}", True, color_texto)
        ventana.blit(msg, (50, 300))
        pygame.display.flip()
        pygame.time.delay(2000)

def ejecutar_juego_ia(jugadores):
    juego = MundoEmpresarial(jugadores)
    objetivo_secreto = random.choice(OBJETIVOS_SECRETOS)

    for ronda in range(1, 4):
        VENTANA.fill(COLOR_FONDO)
        titulo = FUENTE.render(f"Ronda IA {ronda}", True, COLOR_TEXTO)
        pista = FUENTE_SMALL.render(f"Pista: {objetivo_secreto['pista']}", True, COLOR_TEXTO)
        VENTANA.blit(titulo, (50, 30))
        VENTANA.blit(pista, (50, 80))

        juego.generar_empresas()

        for idx, jugador in enumerate(juego.jugadores):
            color = COLORES_JUGADORES[idx % len(COLORES_JUGADORES)]
            info = f"{jugador.nombre} | Dinero: ${jugador.dinero} | Empresas: {', '.join([e.nombre for e in jugador.empresas])}"
            render = FUENTE_SMALL.render(info, True, color)
            VENTANA.blit(render, (50, 140 + idx * 40))

        pygame.display.flip()
        pygame.time.delay(2000)

        for ia in [j for j in juego.jugadores if isinstance(j, IAJugador)]:
            ventas = decidir_ventas_ia(ia)
            for empresa, precio, razon in ventas:
                ia.empresas.remove(empresa)
                ia.dinero += precio
                VENTANA.fill(COLOR_FONDO)
                msg = FUENTE_SMALL.render(f"{ia.nombre} vendió {empresa.nombre} por ${precio} ({razon})", True, COLOR_TEXTO)
                VENTANA.blit(msg, (50, 300))
                pygame.display.flip()
        pygame.time.delay(1000)


        # Subasta automática para cada empresa
        for emp in juego.empresas_disponibles[:]:  # Copia para iterar mientras se modifica
            iniciar_subasta_ia(emp, juego.jugadores)

        juego.empresas_disponibles = [e for e in juego.empresas_disponibles if e.esta_disponible()]
        for jugador in juego.jugadores:
            aplicar_ventajas(jugador)
        juego.ronda += 1

        for ia in [j for j in jugadores if isinstance(j, IAJugador)]:
            registro_ia.append({
                "ronda": ronda,
                "nombre": ia.nombre,
                "dinero": ia.dinero,
                "empresas": len(ia.empresas),
                "tipos": list(ia.contar_por_tipo().keys()),
                "valor_total": ia.valor_total(),
                "objetivo_secreto_cumplido": objetivo_secreto["condicion"](ia)
            })

    # Mostrar resultados
    VENTANA.fill(COLOR_FONDO)
    titulo = FUENTE.render("RESULTADOS IAs:", True, COLOR_TEXTO)
    VENTANA.blit(titulo, (50, 30))

    ganador_secreto = next((j for j in jugadores if objetivo_secreto["condicion"](j)), None)

    if ganador_secreto:
        texto = FUENTE_SMALL.render(f"¡{ganador_secreto.nombre} cumplió el objetivo secreto!", True, COLOR_TEXTO)
        VENTANA.blit(texto, (50, 100))
        texto2 = FUENTE_SMALL.render(f"Objetivo: {objetivo_secreto['descripcion']}", True, COLOR_TEXTO)
        VENTANA.blit(texto2, (50, 140))
    else:
        jugadores_ordenados = sorted(jugadores, key=lambda j: j.valor_total(), reverse=True)
        for i, j in enumerate(jugadores_ordenados):
            texto = FUENTE_SMALL.render(f"{i+1}. {j.nombre} - Valor total: ${j.valor_total()}", True, COLOR_TEXTO)
            VENTANA.blit(texto, (50, 100 + i * 40))

    pygame.display.flip()
    pygame.time.delay(5000)

def iniciar_subasta_ia(empresa, jugadores):
    oferta_actual = empresa.valor // 2
    mejor_postor = None
    hubo_puja = False

    for i in range(5):  # Hasta 5 rondas de puja IA
        pygame.time.delay(1000)
        VENTANA.fill(COLOR_FONDO)
        titulo = FUENTE.render(f"Subasta IA: {empresa.nombre}", True, COLOR_TEXTO)
        VENTANA.blit(titulo, (50, 30))
        VENTANA.blit(FUENTE_SMALL.render(f"Valor base: ${empresa.valor}", True, COLOR_TEXTO), (50, 80))
        VENTANA.blit(FUENTE_SMALL.render(f"Oferta actual: ${oferta_actual}", True, COLOR_TEXTO), (50, 120))

        y = 160
        postores = []

        for ia in [j for j in jugadores if isinstance(j, IAJugador)]:
            if ia.dinero > oferta_actual + 100 and random.random() < 0.6:
                oferta_actual += 100
                mejor_postor = ia
                postores.append(f"{ia.nombre} puja ${oferta_actual}")
                hubo_puja = True
                break  # Solo una IA puja por ronda para hacer la animación pausada

        for postor in postores:
            VENTANA.blit(FUENTE_SMALL.render(postor, True, COLOR_TEXTO), (50, y))
            y += 30

        pygame.display.flip()

        if not postores:
            pygame.time.delay(1000)

    if mejor_postor:
        mejor_postor.dinero -= oferta_actual
        mejor_postor.empresas.append(empresa)
        empresa.propietario = mejor_postor
        VENTANA.fill(COLOR_FONDO)
        mensaje = FUENTE.render(f"{mejor_postor.nombre} ganó por ${oferta_actual}", True, COLOR_TEXTO)
        VENTANA.blit(mensaje, (50, 300))
        pygame.display.flip()
        pygame.time.delay(2000)
    else:
        VENTANA.blit(FUENTE_SMALL.render("Nadie pujó. Subasta cancelada.", True, COLOR_TEXTO), (50, y + 30))
        pygame.display.flip()
        pygame.time.delay(2000)

def decidir_ventas_ia(ia):
    empresas_a_vender = []
    for emp in ia.empresas:
        # Criterios negativos (no vender)
        if emp.ventaja and "Dominio" in emp.ventaja:
            continue
        if ia.estrategia == "acaparadora" and ia.contar_por_tipo()[emp.tipo] <= 1:
            continue
        if ia.dinero > 2000 and random.random() < 0.5:
            continue  # no necesita vender aún

        # Criterios positivos
        razon = ""
        precio_base = emp.valor

        if ia.dinero < 1000:
            razon = "💸 Necesita liquidez"
            precio_venta = int(precio_base * 0.9)
        elif emp.ventaja:
            razon = "🎯 Vende con ventaja"
            precio_venta = int(precio_base * 1.3)
        else:
            razon = "🤝 Venta estratégica"
            precio_venta = int(precio_base * random.uniform(1.1, 1.2))

        empresas_a_vender.append((emp, precio_venta, razon))
    return empresas_a_vender


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
