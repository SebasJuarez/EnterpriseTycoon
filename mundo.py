import random
from empresa import Empresa

class MundoEmpresarial:
    def __init__(self, jugadores):
        self.jugadores = jugadores
        self.empresas_disponibles = []
        self.ronda = 1

        self.catalogo_empresas = [
            Empresa("Google", "tecnologia", 3000, 1, "Dominio en publicidad", efecto="bono_publicidad"),
            Empresa("Pfizer", "salud", 2800, 1, "Acceso a patentes exclusivas", efecto="bono_patente"),
            Empresa("Netflix", "medios", 2500, 1, "Popularidad global", efecto="bono_popularidad"),
            Empresa("Goldman Sachs", "finanzas", 2700, 1, "Red de inversión privilegiada", efecto="bono_inversion"),
            Empresa("Meta", "tecnologia", 3200, 2, "Integración de plataformas", efecto="bono_sinergia"),
            Empresa("Roche", "salud", 2900, 2, "Dominio en biotecnología", efecto="bono_ciencia"),
            Empresa("SpaceX", "tecnologia", 3500, 2, "Acceso a tecnología espacial", efecto="bono_innovacion"),
            Empresa("Twitter", "medios", 1500, 1, None),
            Empresa("BlackRock", "finanzas", 3800, 3, "Manipulación de mercado", efecto="bono_ventas"),
            Empresa("Epic Games", "entretenimiento", 2200, 1, "Monetización agresiva", efecto="bono_liquidez"),
            Empresa("Shell", "energia", 3000, 2, "Acceso global de infraestructura", efecto="bono_logistica"),
            Empresa("Tesla", "tecnologia", 3300, 2, "Innovación disruptiva", efecto="bono_innovacion"),
            Empresa("WeWork", "inmobiliario", 1000, 1, "Liquidez inmediata (pierde turno)", efecto="pierde_turno"),
            Empresa("Theranos", "salud", 800, 1, "Pierde $500 tras 2 rondas", efecto="castigo_dinero_2r"),
            Empresa("ByteDance", "tecnologia", 2800, 2, "Dominio en redes sociales", efecto="bono_popularidad"),
            Empresa("Reddit", "medios", 1800, 1, None),
            Empresa("OpenAI", "tecnologia", 3600, 3, "Ventaja en algoritmos", efecto="bono_ia"),
        ]


        self.catalogo_disponible = self.catalogo_empresas.copy()

    def generar_empresas(self):
        random.shuffle(self.catalogo_disponible)
        nuevas = []

        while self.catalogo_disponible and len(nuevas) < 3:
            empresa = self.catalogo_disponible.pop(0)
            if empresa.esta_disponible():
                nuevas.append(empresa)

        self.empresas_disponibles.extend(nuevas)
    
    def ejecutar_eventos(self):
        if not hasattr(self, "eventos_programados"):
            self.eventos_programados = []

        for evento in self.eventos_programados[:]:
            ronda_objetivo, jugador, cantidad = evento
            if self.ronda == ronda_objetivo:
                jugador.dinero -= cantidad
                print(f"{jugador.nombre} pierde ${cantidad} por penalización programada.")
                self.eventos_programados.remove(evento)

    def agendar_castigo(self, jugador, rondas_despues, cantidad):
        if not hasattr(self, "eventos_programados"):
            self.eventos_programados = []
        ronda_objetivo = self.ronda + rondas_despues
        self.eventos_programados.append((ronda_objetivo, jugador, cantidad))


    def ejecutar_ronda(self):
        print(f"\n--- Ronda {self.ronda} ---")

        self.ejecutar_eventos() 
        self.generar_empresas()

        for jugador in self.jugadores:
            if hasattr(jugador, "saltar_turno") and jugador.saltar_turno:
                print(f"{jugador.nombre} pierde este turno por penalización.")
                jugador.saltar_turno = False
                continue

            jugador.tomar_turno(self.empresas_disponibles, self.jugadores, self)

        self.empresas_disponibles = [e for e in self.empresas_disponibles if e.esta_disponible()]
        self.ronda += 1

